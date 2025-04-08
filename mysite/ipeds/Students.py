
class Students:
    def __init__(self, term):
        self.term = term

    def base(self):
        query = f"""
        SELECT DISTINCT STUDENT_ID AS ID
        FROM STUDENT_ENROLLMENT_VIEW
        WHERE ENROLL_CURRENT_STATUS IN ('New', 'Add')
        AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)
        AND ENROLL_TERM = '{self.term}'
        """
        return query

    def gender(self):
        query = """
        SELECT ID AS X,
               GENDER AS Y
        FROM PERSON
        """
        return query

    def race(self):
        query = """
        SELECT ID AS X,
                IPEDS_RACE_ETHNIC_DESC AS Y
        FROM Z01_ALL_RACE_ETHNIC_W_FLAGS
        """
        return query

    def join_table_dict(self, feature):
        if feature == 'GENDER': return self.gender()
        if feature == 'RACE': return self.race()

    def table(self, *features):
        query = f"""
        SELECT ID
        FROM ({self.base()}) AS STUDENTS
        """
        return query



