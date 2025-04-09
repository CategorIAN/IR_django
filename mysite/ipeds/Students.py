
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

    def status(self):
        query = f"""
        SELECT STUDENT_ID AS X,
               CASE
               WHEN STP_PROGRAM_TITLE = 'Non-Degree Seeking Students' THEN 'Non-Degree Seeking'
               WHEN FM.TERM = '{self.term}' THEN CASE
                    WHEN STPR_ADMIT_STATUS = 'FY' THEN 'First-time' ELSE 'Transfer-in' END
               ELSE 'Continuing/Returning' END AS Y
        FROM (
            SELECT * FROM (
                SELECT STUDENT_ID,
                        STP_PROGRAM_TITLE,
                        ROW_NUMBER() OVER (PARTITION BY STUDENT_ID 
                        ORDER BY CASE WHEN STP_END_DATE IS NULL THEN 0 ELSE 1 END, STP_END_DATE DESC) AS PROGRAM_RANK
                FROM STUDENT_ACAD_PROGRAMS_VIEW
                WHERE STP_START_DATE <= (SELECT TOP 1 TERMS.TERM_END_DATE FROM TERMS WHERE TERMS_ID = '{self.term}')
            ) ranked
            WHERE PROGRAM_RANK = 1) AS SAPV
        LEFT JOIN (
            SELECT STPR_STUDENT, STPR_ADMIT_STATUS
            FROM (
                SELECT STPR_STUDENT,
                        STPR_ADMIT_STATUS,
                        ROW_NUMBER() OVER (PARTITION BY STPR_STUDENT ORDER BY STUDENT_PROGRAMS_ADDDATE) AS ADMIT_RANK
                FROM STUDENT_PROGRAMS_VIEW
                ) ranked
                WHERE ADMIT_RANK = 1) AS FIRST_ADMIT ON SAPV.STUDENT_ID = FIRST_ADMIT.STPR_STUDENT
        LEFT JOIN Z01_AAV_STUDENT_FIRST_MATRIC AS FM ON SAPV.STUDENT_ID = FM.ID
        """
        return query

    def load(self):
        query = f"""
        SELECT DISTINCT STUDENT_ID AS X,
                CASE WHEN STUDENT_LOAD IN ('F', 'O') THEN 'Full-Time' ELSE 'Part-Time' END AS Y
        FROM STUDENT_ENROLLMENT_VIEW
        WHERE ENROLL_TERM = '{self.term}'
        """
        return query

    def acad_level(self):
        query = f"""
        SELECT DISTINCT STUDENT_ID AS X,
                CASE
                WHEN STUDENT_ACAD_LEVEL = 'UG' THEN 'Undergraduate'
                WHEN STUDENT_ACAD_LEVEL = 'GR' THEN 'Graduate' END AS Y
        FROM STUDENT_ENROLLMENT_VIEW
        WHERE ENROLL_TERM = '{self.term}'
        """
        return query

    def cip_class(self):
        query = f"""
        SELECT STUDENT_ID AS X,
                CASE
                    WHEN ACPG_CIP LIKE '13%' THEN 'Education'
                    WHEN ACPG_CIP LIKE '14%' THEN 'Engineering'
                    WHEN ACPG_CIP LIKE '26%' THEN 'Biological and Biomedical Sciences'
                    WHEN ACPG_CIP LIKE '27%' THEN 'Mathematics and Statistics'
                    WHEN ACPG_CIP LIKE '40%' THEN 'Physical Sciences'
                    WHEN ACPG_CIP LIKE '52%' THEN 'Business, Management, Marketing and Related Support Services'
                END AS Y
        FROM (
            SELECT * FROM (
                SELECT STUDENT_ID,
                        STP_ACADEMIC_PROGRAM,
                        ROW_NUMBER() OVER (PARTITION BY STUDENT_ID 
                        ORDER BY CASE WHEN STP_END_DATE IS NULL THEN 0 ELSE 1 END, STP_END_DATE DESC) AS PROGRAM_RANK
                FROM STUDENT_ACAD_PROGRAMS_VIEW
                WHERE STP_START_DATE <= (SELECT TOP 1 TERMS.TERM_END_DATE FROM TERMS WHERE TERMS_ID = '{self.term}')
            ) ranked
            WHERE PROGRAM_RANK = 1) AS SAPV
        JOIN ACAD_PROGRAMS ON SAPV.STP_ACADEMIC_PROGRAM = ACAD_PROGRAMS_ID
        """
        return query

    def join_table_dict(self, feature):
        if feature == 'GENDER': return self.gender()
        if feature == 'RACE': return self.race()
        if feature == 'STATUS': return self.status()
        if feature == 'LOAD': return self.load()
        if feature == 'ACAD_LEVEL': return self.acad_level()
        if feature == 'CIP_CLASS': return self.cip_class()

    def table(self, features):
        query = f"""
        SELECT ID, 
               {",\n               ".join([f"{feature}_TABLE.Y AS {feature}" for feature in features])}
        FROM ({self.base()}) AS STUDENTS
        {"\n        ".join([f"JOIN ({self.join_table_dict(feature)}) AS {feature}_TABLE ON ID = {feature}_TABLE.X"
                    for feature in features])}
        """
        return query



