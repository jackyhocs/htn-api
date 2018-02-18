import sqlite3
import json


#Setting up connections to the DBs
connUser = sqlite3.connect('users.db', check_same_thread=False)
connUser.row_factory = sqlite3.Row
c = connUser.cursor()

connSkills = sqlite3.connect('skills.db', check_same_thread=False)
connSkills.row_factory = sqlite3.Row
cSkills = connSkills.cursor()


class UserDao():
    @classmethod
    def get_by_id(cls, _id) -> dict:
        '''
        Gets the User by ID
        :param _id:
        :return:
        Dictionary of the User or an exception if the user does not exist/was deleted
        '''
        try:
            #Selecting and returning the row with the specified user
            c.execute("SELECT * FROM USERS WHERE id=:id", {'id': _id})
            user = c.fetchone()
        except sqlite3.Error as e:
            raise sqlite3.DatabaseError from e

        #if user does not exist, raise an exception so app can return 404
        if not user:
            raise sqlite3.DataError

        #return dictionary of the user
        return dict(user)

    @classmethod
    def get_all_users(cls):
        '''
        Gets all Users in the database
        :return:
        Returns a list of dictionaries of the Users
        '''
        try:
            #Selecting all users and returning the entire DB of users
            c.execute("SELECT * FROM USERS")
            users = c.fetchall()
        except sqlite3.Error as e:
            raise sqlite3.DatabaseError from e

        #Changes the list of sqlite.Rows to a list of dictionaries before returning
        users_collection = [dict(user) for user in users]

        return users_collection

    @classmethod
    def delete_user(cls, _id):
        '''
        Deletes the user with the specified ID and
        performs the necessary updates to the Skills table
        :param _id:
        :return:
        '''
        with connUser:
            #Find the user, if the user does not exist, get_by_id will raise the correct exceptions
            user = cls.get_by_id(_id)
            with connSkills:
                try:
                    #Update the Skills table by removing the User's skills from the values
                    for skill in json.loads(user['skills']):
                        skillname = skill['name']
                        value = skill['rating']
                        cSkills.execute("UPDATE SKILLS SET num_users = num_users - 1 AND \
                        total_rating = (total_rating - :value) AND avg_rating = (total_rating-:value)/(num_users - 1) WHERE skill = :skill",
                                        {
                                            'skill': skillname,
                                            'value': value
                                        })
                    connSkills.close()

                except sqlite3.Error as e:
                    connSkills.close()
                    raise sqlite3.DatabaseError from e

            try:
                #Deletes the user from the USERS table
                c.execute("DELETE from USERS WHERE id = :id",
                      {'id': _id})
                deleted = c.execute("SELECT changes()")
            except sqlite3.Error as e:
                raise sqlite3.DatabaseError from e

            #if no row was deleted, then an exception is raised - 409 conflict
            if not deleted:
                raise sqlite3.DataError

    @classmethod
    def update_user(cls, _id, payload):
        '''
        Performs an update with a validated payload and
        performs the necessary changes to the Skills table
        :param _id:
        :param payload:
        :return:
        Dictionary of the new user
        '''
        #Checks if the user exists
        existing = cls.get_by_id(_id)

        #Saves the old list of skills for updating the Skills table
        oldskills = existing['skills']

        #changes the dictionary to have the updated fields passed in through the payload
        existing.update(**payload)
        existing['id'] = _id
        with connUser:
            try:
                #Updates the user's stats from the payload
                c.execute("UPDATE USERS SET name = :name, company = :company, \
                                email = :email, latitude = :latitude, longitude = :longitude,\
                                picture = :picture, skills = :skills, phone = :phone WHERE id = :id",
                          existing)
            except sqlite3.Error as e:
                connUser.close()
                raise sqlite3.DatabaseError from e
        connUser.close()

        #Here, we have to update the Skills table because the payload could have either added or removed skills
        with connSkills:
            try:
                #updatedSkills stores the delta in the values
                # positive values means that the rating will increase
                # negative will mean that the value either was removed or decreased
                updatedSkills = {}
                
                #Iterates through the old list of skills to check for any decreases
                for skill in oldskills:
                    if skill['name'] in payload:
                        #if there is a new value given by the payload, set the delta to the value with the key of the skill
                        updatedSkills[skill['name']] = payload[skill['rating']] - skill['rating']
                    else:
                        #otherwise, the skill was deleted, so we set the delta to the negative value of the rating
                        updatedSkills[skill['name']] = - skill['rating']
                
                #Iterate through the new payload to check if there's an entirely new skill that was added
                for skill in payload:
                    if skill['name'] not in updatedSkills:
                        #A new skill was added so we set the delta to the rating
                        updatedSkills[payload['skill']] = payload['rating']
                    else:
                        #The value has been looked over while iterating through oldskills
                        pass

                #perform the updates
                with connSkills:
                    for skill in updatedSkills:
                        cSkills.execute("UPDATE SKILLS SET num_users = num_users + :user_diff AND\
                        total_rating = total_rating +:rating_diff AND avg_rating = (total_rating +:ratingdiff)/(num_users + :user_diff)\
                        WHERE skill = :skill",
                                        {
                                            'skill': skill['name'],
                                            'rating_diff': skill['rating'],
                                            'user_diff': 1 if skill['rating'] > 0 else -1
                                        })
            except sqlite3.Error as e:
                connSkills.close()
                raise sqlite3.DatabaseError from e
            connSkills.close()

        #Returns the new dictionary of the User
        return cls.get_by_id(_id)

    @classmethod
    def find_skill_by_params(cls, payload):
        '''
        Returns the row of the Skills table with respect to the payload
        :param payload:
        :return:
        List of dictionaries that match the specified input
        '''

        query = "SELECT * FROM SKILLS WHERE"
        #and_append is just there for adding AND to the query when multiple items are in the payload
        and_append = False
        if 'skill' in payload:
            query += " skill = :skill"
            and_append = True
            
        if 'rating' in payload:
            if and_append:
                query += " AND"
            query += " avg_rating >= :rating"
            and_append = True

        if 'frequency' in payload:
            if and_append:
                query += " AND"
            query += " num_users >= :frequency"

        try:
            #Executes the query to find the number of matched results
            cSkills.execute(query, payload)
            skills = cSkills.fetchall()
        except sqlite3.Error as e:
            raise sqlite3.DatabaseError from e

        #We do not raise the NotFound exception, we just return a list showing that nothing matched
        if not skills:
            return [{"count": 0}]

        #Otherwise, we create a list of dictionaries of the Rows of matches
        skill_collection = [dict(skill) for skill in skills]

        #Insert the count at index 0 of the list
        count = len(skill_collection)
        skill_collection.insert(0, {'count': count})

        #return the list of the skills
        return skill_collection

