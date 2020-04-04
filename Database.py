import sqlite3 as lite
from enum import Enum

from PyQt5.QtGui import QPixmap


class KEYS(Enum):
    LOCATION = 'location'
    CARID = 'carid'
    CARCOLOR = 'carcolor'
    FIRSTSIGHTED = 'firstsighted'
    CARIMAGE = 'carimage'
    LICENSENUMBER = 'licensenumber'
    LICENSEIMAGE = 'licenseimage'
    NUMRULESBROKEN = 'numrulesbroken'
    CAROWNER = 'carowner'
    RULENAME = 'rulename'
    RULEFINE = 'rulefine'
    TIME = 'time'
    RULEID = 'ruleid'


class Database:
    __instance = None

    @staticmethod
    def get_instance():
        if Database.__instance is None:
            Database()
        return Database.__instance

    def __init__(self):
        if Database.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Database.__instance = self
            self.con = lite.connect("database/traffic.db")

    def get_car_color_list(self):
        command = "select distinct(color) from cars"
        rows = self.con.cursor().execute(command).fetchall()
        return [row[0] for row in rows]

    def get_licenses(self):
        command = "select license_number from cars"
        rows = self.con.cursor().execute(command).fetchall()
        return [row[0] for row in rows]

    def insert_into_cars(self, car_id='', color='', lic_num='', lic_img='', car_img='', owner=''):
        sql = '''INSERT INTO cars(id, color,license_image, license_number, car_image, owner)
                      VALUES(?,?,?,?,?,?) '''

        car_img = car_img.split('/')[-1]
        lic_img = lic_img.split('/')[-1]
        cur = self.con.cursor()
        cur.execute(sql, (car_id, color, lic_num, lic_img, car_img, owner))
        cur.close()
        self.con.commit()

    def get_max_car_id(self):
        sql = '''select max(id) from cars'''
        carid = self.con.cursor().execute(sql).fetchall()[0][0]
        if carid is None:
            carid = 1
        return carid

    def insert_into_violations(self, camera, car, rule, time):
        sql = '''INSERT INTO violations(camera, car, rule, time)
                      VALUES(?,?,?,?) '''
        cur = self.con.cursor()
        cur.execute(sql, (camera, car, rule, self.covert_time_to_bd(time)))
        cur.close()
        self.con.commit()

    def insert_into_rules(self, rule, fine):
        sql = '''INSERT INTO rules(name, fine)
                      VALUES(?,?) '''
        cur = self.con.cursor()
        cur.execute(sql, (rule, fine))
        cur.close()
        self.con.commit()

    def insert_into_camera(self, id, location, x, y, group, file):
        sql = '''INSERT INTO camera(id,location,coordinate_x, coordinate_y, feed, cam_group)
                      VALUES(?,?,?,?,?,?) '''
        file = file.split('/')[-1]
        cur = self.con.cursor()
        cur.execute(sql, (id, location, x, y, file, group))
        cur.close()
        self.con.commit()

    def search(self, cam=None, color=None, license=None, time=None):
        cur = self.con.cursor()
        command = "SELECT camera.location, cars.id, cars.color, cars.first_sighted, cars.license_image, " \
                  " cars.license_number, cars.car_image, cars.num_rules_broken, cars.owner," \
                  " rules.name, rules.fine, violations.time, rules.id" \
                  " FROM violations, rules, cars, camera" \
                  " where rules.id = violations.rule" \
                  " and violations.camera = camera.id" \
                  " and cars.id = violations.car"

        if cam is not None:
            command = command + " and violations.camera = '" + str(cam) + "'"
        if color is not None:
            command = command + " and cars.color = '" + str(color) + "'"
        if time is not None:
            command = command + " and violations.time >= " + str(
                self.covert_time_to_bd(time[0])) + " and violations.time <= " + str(self.covert_time_to_bd(time[1]))

        cur.execute(command)
        rows = cur.fetchall()
        ret = []
        for row in rows:
            ret.append({
                KEYS.LOCATION: row[0],
                KEYS.CARID: row[1],
                KEYS.CARCOLOR: row[2],
                KEYS.FIRSTSIGHTED: row[3],
                KEYS.CARIMAGE: QPixmap("car_images/" + row[4]),
                KEYS.LICENSENUMBER: row[5],
                KEYS.LICENSEIMAGE: QPixmap("license_images/" + row[6]),
                KEYS.NUMRULESBROKEN: row[7],
                KEYS.CAROWNER: row[8],
                KEYS.RULENAME: row[9],
                KEYS.RULEFINE: row[10],
                KEYS.TIME: row[11],
                KEYS.RULEID: row[12],
            })
        cur.close()
        return ret

    def get_violations_from_cam(self, cam, cleared=False):
        cur = self.con.cursor()
        command = "SELECT camera.location, cars.id, cars.color, cars.first_sighted, cars.license_image, " \
                  " cars.license_number, cars.car_image, cars.num_rules_broken, cars.owner," \
                  " rules.name, rules.fine, violations.time, rules.id" \
                  " FROM violations, rules, cars, camera" \
                  " where rules.id = violations.rule" \
                  " and cars.id = violations.car" \
                  " and violations.camera = camera.id"
        if cam is not None:
            command = command + " and violations.camera = '" + str(cam) + "'"
        if cleared:
            command = command + " and violations.cleared = true"
        else:
            command = command + " and violations.cleared = false"

        cur.execute(command)
        rows = cur.fetchall()
        ret = []
        for row in rows:
            ret.append({
                KEYS.LOCATION: row[0],
                KEYS.CARID: row[1],
                KEYS.CARCOLOR: row[2],
                KEYS.FIRSTSIGHTED: row[3],
                KEYS.CARIMAGE: QPixmap("car_images/" + row[6]),
                KEYS.LICENSENUMBER: row[5],
                KEYS.LICENSEIMAGE: QPixmap("license_images/" + row[6]),
                KEYS.NUMRULESBROKEN: row[7],
                KEYS.CAROWNER: row[8],
                KEYS.RULENAME: row[9],
                KEYS.RULEFINE: row[10],
                KEYS.TIME: row[11],
                KEYS.RULEID: row[12],

            })
        cur.close()
        return ret

    def delete_violation(self, carid, ruleid, time):
        cur = self.con.cursor()
        command = "update violations set cleared = true " \
                  "where car = " + str(carid) + " and rule = " + str(ruleid) + " and time = " + str(time)
        rowcount = cur.execute(command).rowcount
        print("Deleted " + str(rowcount) + " rows")
        cur.close()
        self.con.commit()

    def get_cam_details(self, cam_id):
        command = "select count(*) from violations where camera = '" + str(cam_id) + "'"
        cur = self.con.cursor()
        count = cur.execute(command).fetchall()[0][0]
        cur.close()

        command = "select location, feed from camera where id = '" + str(cam_id) + "'"
        cur = self.con.cursor()
        res = cur.execute(command).fetchall()
        location = None
        feed = None
        location, feed = res[0]
        cur.close()
        return count, location, feed

    def delete_all_cars(self):
        commad = "delete from cars"
        cur = self.con.cursor()
        cur.execute(commad)
        cur.close()
        self.con.commit()

    def delete_all_violations(self):
        commad = "delete from violations"
        cur = self.con.cursor()
        cur.execute(commad)
        cur.close()
        self.con.commit()

    def get_cam_list(self, group):
        if group is not None:
            command = "select id, location, feed from camera where cam_group = '{}'".format(str(group))
        else:
            command = "select id, location, feed from camera"

        cur = self.con.cursor()
        cur.execute(command)
        rows = cur.fetchall()
        ret = [(row[0], row[1], row[2]) for row in rows]
        cur.close()
        return ret

    def get_cam_group_list(self):
        command = "select name from camera_group"
        cur = self.con.cursor()
        cur.execute(command)
        rows = cur.fetchall()
        ret = [row[0] for row in rows]
        cur.close()
        return ret

    def clear_cam_log(self):
        command = "update violations set cleared = true"
        cur = self.con.cursor()
        cur.execute(command)
        cur.close()
        self.con.commit()

    def covert_time_to_bd(self, time):
        pass

    def convert_time_to_GUI(self, time):
        pass
