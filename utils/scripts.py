from django.db import connection


class Script:

    def run(self):
        raise NotImplementedError


class DBScript(Script):


    def enable_rls_on_company(self):
        with connection.cursor() as cursor:
            cursor.execute("ALTER TABLE company_company ENABLE ROW LEVEL SECURITY;")
            cursor.execute("ALTER TABLE company_company FORCE ROW LEVEL SECURITY;")
            cursor.execute(
                "CREATE POLICY company_policy ON company_company FOR SELECT USING (created_by_id = current_user::uuid);"
            )
            cursor.execute(
                "CREATE POLICY company_update_policy ON company_company FOR UPDATE USING (created_by_id = current_user::uuid);"
            )

    def enable_rls_on_project(self):
        with connection.cursor() as cursor:
            cursor.execute("ALTER TABLE company_project ENABLE ROW LEVEL SECURITY;")
            cursor.execute("ALTER TABLE company_project FORCE ROW LEVEL SECURITY;")
            cursor.execute(
                "CREATE POLICY project_select_policy ON company_project FOR SELECT USING (company_id IN (SELECT id FROM company_company WHERE created_by_id = current_user::uuid));"
            )
            cursor.execute(
                "CREATE POLICY project_update_policy ON company_project FOR UPDATE USING (company_id IN (SELECT id FROM company_company WHERE created_by_id = current_user::uuid));"
            )

    def enable_rls_on_environment(self):
         with connection.cursor() as cursor:
            cursor.execute(
                "ALTER TABLE company_environment ENABLE ROW LEVEL SECURITY;"
            )
            cursor.execute("ALTER TABLE company_environment FORCE ROW LEVEL SECURITY;")
            cursor.execute(
                "CREATE POLICY environment_select_policy ON company_environment FOR SELECT USING (project_id IN (SELECT id FROM company_project WHERE company_id IN (SELECT id FROM company_company WHERE created_by_id = current_user::uuid)));"
            )
            cursor.execute(
                "CREATE POLICY environment_update_policy ON company_environment FOR UPDATE USING (project_id IN (SELECT id FROM company_project WHERE company_id IN (SELECT id FROM company_company WHERE created_by_id = current_user::uuid)));"
            )

    def enable_rls_on_db_schemas(self):
         with connection.cursor() as cursor:
            cursor.execute("ALTER TABLE company_dbschema ENABLE ROW LEVEL SECURITY;")
            cursor.execute("ALTER TABLE company_dbschema FORCE ROW LEVEL SECURITY;")
            cursor.execute(
                "CREATE POLICY dbschema_select_policy ON company_dbschema FOR SELECT USING (project_id IN (SELECT id FROM company_project WHERE company_id IN (SELECT id FROM company_company WHERE created_by_id = current_user::uuid)));"
            )
            cursor.execute(
                "CREATE POLICY dbschema_update_policy ON company_dbschema FOR UPDATE USING (project_id IN (SELECT id FROM company_project WHERE company_id IN (SELECT id FROM company_company WHERE created_by_id = current_user::uuid)));"
            )

    def enable_rls_on_db_secret(self):
         with connection.cursor() as cursor:
            cursor.execute("ALTER TABLE company_dbsecret ENABLE ROW LEVEL SECURITY;")
            cursor.execute("ALTER TABLE company_dbsecret FORCE ROW LEVEL SECURITY;")
            cursor.execute(
                "CREATE POLICY dbsecret_select_policy ON company_dbsecret FOR SELECT USING (company_id IN (SELECT id FROM company_company WHERE created_by_id = current_user::uuid));"
            )
            cursor.execute(
                "CREATE POLICY dbsecret_update_policy ON company_dbsecret FOR UPDATE USING (company_id IN (SELECT id FROM company_company WHERE created_by_id = current_user::uuid));"
            )

    def enable_rls_on_apis(self):
         with connection.cursor() as cursor:
            cursor.execute("ALTER TABLE company_api ENABLE ROW LEVEL SECURITY;")
            cursor.execute("ALTER TABLE company_api FORCE ROW LEVEL SECURITY;")
            cursor.execute(
                "CREATE POLICY api_select_policy ON company_api FOR SELECT USING (project_id IN (SELECT id FROM company_project WHERE company_id IN (SELECT id FROM company_company WHERE created_by_id = current_user::uuid)));"
            )
            cursor.execute(
                "CREATE POLICY api_update_policy ON company_api FOR UPDATE USING (project_id IN (SELECT id FROM company_project WHERE company_id IN (SELECT id FROM company_company WHERE created_by_id = current_user::uuid)));"
            )

    def run(self):

        # helps in raising error correctly
        func_ns = [
            "company",
            "project",
            "environment",
            "db_schemas",
            "db_secret",
            "apis",
        ]

        for func_n in func_ns:
            try:
                fn = f"enable_rls_on_{func_n}"
                func = getattr(self, fn)
                func()
            except Exception as e:
                print(e)


db_script = DBScript()
run = db_script.run