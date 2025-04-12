
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

    def assigned_gender(self):
        query = """
        SELECT PERSON.ID AS X,
                COALESCE(GENDER, ASSIGNED_GENDER.Y) AS Y
        FROM PERSON
        LEFT JOIN (VALUES 
                    (6189200, 'M'),
                    (6189204, 'M'),
                    (6189252, 'M'),
                    (6186217, 'M'),
                    (6190237, 'M'),
                    (6190238, 'M'),
                    (6190246, 'M'),
                    (6189572, 'M'),
                    (6189318, 'M'),
                    (6189974, 'M'),
                    (6189975, 'M'),
                    (6189977, 'M'),
                    (6187468, 'M'),
                    (6189635, 'M'),
                    (6190236, 'M'),
                    (6189662, 'M'),
                    (6189973, 'M'),
        -----------------------------------------------------
                    (6184697, 'F'),
                    (6184977, 'F'),
                    (6189250, 'F'),
                    (6185039, 'F'),
                    (6178065, 'F'),
                    (6178068, 'F'),
                    (6189523, 'F'),
                    (6190232, 'F'),
                    (6190233, 'F'),
                    (6190235, 'F'),
                    (6190242, 'F'),
                    (6189571, 'F'),
                    (6187470, 'F'),
                    (6187467, 'F'),
                    (6188541, 'F'),
                    (6188544, 'F'),
                    (6188940, 'F'),
                    (6189317, 'F'),
                    (6188731, 'F'),
                    (6188797, 'F'),
                    (6189969, 'F'),
                    (6189970, 'F'),
                    (6189971, 'F'),
                    (6189972, 'F'),
                    (6189978, 'F'),
                    (6190240, 'F'),
                    (6186670, 'F'),
                    (6184447, 'F'),
                    (6189976, 'F'),
                    (6178066, 'F'),
                    (6188264, 'F'),
                    (6189575, 'F'),
                    (6190234, 'F'),
                    (6188723, 'F')
                    ) AS ASSIGNED_GENDER(ID, Y) ON PERSON.ID = ASSIGNED_GENDER.ID
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
                    WHEN ACPG_CIP LIKE '13%' THEN '13'
                    WHEN ACPG_CIP LIKE '14%' THEN '14'
                    WHEN ACPG_CIP LIKE '26%' THEN '26'
                    WHEN ACPG_CIP LIKE '27%' THEN '27'
                    WHEN ACPG_CIP LIKE '40%' THEN '40'
                    WHEN ACPG_CIP LIKE '52%' THEN '52'
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
        if feature == 'ASSIGNED_GENDER': return self.assigned_gender()
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

    def filtered(self, x, filter_by):
        query = f"""
        SELECT *
        FROM ({x}) AS STUDENTS
        WHERE {"\nAND ".join([f"{k} = '{v}'" for k, v in filter_by.items()])}
        """
        return query

    def project(self, x, features):
        query = f"""
        SELECT {", ".join(features)}
        FROM ({x}) AS STUDENTS
        """
        return query

    def pivoted(self, x, row_feature, col_feature, columns, col_titles = None):
        col_strs = [f"[{col}]" for col in columns]
        titles = col_strs if col_titles is None else [f"{col} AS {title}" for col, title in zip(col_strs, col_titles)]
        query = f"""
        SELECT {row_feature}, {", ".join(titles)}
        FROM ({x}) AS STUDENTS PIVOT (COUNT(ID) FOR {col_feature} IN ({", ".join(col_strs)})) AS PIVOTED
        """
        return query

    def reordered(self, x, col_feature, ordered_cols):
        col_ordering = zip(ordered_cols, range(len(ordered_cols)))
        query = f"""
        SELECT STUDENTS.*
        FROM ({x}) AS STUDENTS
        JOIN (VALUES {",\n".join([f"('{col}', '{order}')" for col, order in col_ordering])}) AS ORDERING(LABEL, N)
        ON STUDENTS.{col_feature} = ORDERING.LABEL
        ORDER BY ORDERING.N
        """
        return query

    def x(self, load, gender, cip = None):
        table = self.table(['ASSIGNED_GENDER', 'RACE', 'STATUS', 'LOAD', 'ACAD_LEVEL', 'CIP_CLASS'])
        by_cip = {} if cip is None else {'CIP_CLASS': cip}
        filter_by = {'ASSIGNED_GENDER': gender, 'LOAD': load, 'ACAD_LEVEL': 'Undergraduate'} | by_cip
        features = ['ID', 'RACE', 'STATUS']
        q1 = self.project(self.filtered(table, filter_by), features)
        pivot_columns = ['First-time', 'Transfer-in', 'Continuing/Returning', 'Non-Degree Seeking']
        q2 = self.pivoted(q1, 'RACE', 'STATUS', pivot_columns)
        ordered_race = ['U.S. Nonresident',
                        'Hispanic/Latino',
                        'American Indian',
                        'Asian',
                        'Black or African American',
                        'Hawaiian/Pacific Islander',
                        'White',
                        'Two or More Races',
                        'Unknown'
                        ]
        return self.reordered(q2, 'RACE', ordered_race)



