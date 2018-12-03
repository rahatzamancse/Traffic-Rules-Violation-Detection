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


class Database():
    __instance = None

    @staticmethod
    def getInstance():
        if Database.__instance is None:
            Database()
        return Database.__instance

    def __init__(self):
        if Database.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Database.__instance = self
            self.con = lite.connect("database/traffic.db")

    def getCarColorsList(self):
        command = "select distinct(color) from cars"
        rows = self.con.cursor().execute(command).fetchall()
        return [row[0] for row in rows]

    def getLicenseList(self):
        command = "select license_number from cars"
        rows = self.con.cursor().execute(command).fetchall()
        return [row[0] for row in rows]

    def insertIntoCars(self, car_id='', color='', lic_num='', lic_img='', car_img='', owner=''):
        sql = '''INSERT INTO cars(id, color,license_image, license_number, car_image, owner)
                      VALUES(?,?,?,?,?,?) '''

        car_img = car_img.split('/')[-1]
        lic_img = lic_img.split('/')[-1]
        cur = self.con.cursor()
        cur.execute(sql, (car_id, color, lic_num, lic_img, car_img, owner))
        cur.close()
        self.con.commit()

    def getMaxCarId(self):
        sql = '''select max(id) from cars'''
        carid = self.con.cursor().execute(sql).fetchall()[0][0]
        if carid is None:
            carid = 1
        return carid

    def insertIntoViolations(self, camera, car, rule, time):
        sql = '''INSERT INTO violations(camera, car, rule, time)
                      VALUES(?,?,?,?) '''
        cur = self.con.cursor()
        cur.execute(sql, (camera, car, rule, self.convertTimeToDB(time)))
        cur.close()
        self.con.commit()

    def insertIntoRules(self, rule, fine):
        sql = '''INSERT INTO rules(name, fine)
                      VALUES(?,?) '''
        cur = self.con.cursor()
        cur.execute(sql, (rule, fine))
        cur.close()
        self.con.commit()

    def insertIntoCamera(self, id, location, x, y, group, file):
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
                self.convertTimeToDB(time[0])) + " and violations.time <= " + str(self.convertTimeToDB(time[1]))

        cur.execute(command)
        rows = cur.fetchall()
        ret = []
        for row in rows:
            dict = {}
            dict[KEYS.LOCATION] = row[0]
            dict[KEYS.CARID] = row[1]
            dict[KEYS.CARCOLOR] = row[2]
            dict[KEYS.FIRSTSIGHTED] = row[3]

            carimage = QPixmap("car_images/" + row[4])
            dict[KEYS.CARIMAGE] = carimage

            dict[KEYS.LICENSENUMBER] = row[5]

            licenseimage = QPixmap("license_images/" + row[6])
            dict[KEYS.LICENSEIMAGE] = licenseimage

            dict[KEYS.NUMRULESBROKEN] = row[7]
            dict[KEYS.CAROWNER] = row[8]
            dict[KEYS.RULENAME] = row[9]
            dict[KEYS.RULEFINE] = row[10]
            dict[KEYS.TIME] = row[11]
            dict[KEYS.RULEID] = row[12]
            ret.append(dict)
        cur.close()
        return ret

    def getViolationsFromCam(self, cam, cleared=False):
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
            dict = {}
            dict[KEYS.LOCATION] = row[0]
            dict[KEYS.CARID] = row[1]
            dict[KEYS.CARCOLOR] = row[2]
            dict[KEYS.FIRSTSIGHTED] = row[3]

            carImagePath = "car_images/" + row[6]
            carimage = QPixmap(carImagePath)
            dict[KEYS.CARIMAGE] = carimage

            dict[KEYS.LICENSENUMBER] = row[5]

            licenseimage = QPixmap("license_images/" + row[6])
            dict[KEYS.LICENSEIMAGE] = licenseimage

            dict[KEYS.NUMRULESBROKEN] = row[7]
            dict[KEYS.CAROWNER] = row[8]
            dict[KEYS.RULENAME] = row[9]
            dict[KEYS.RULEFINE] = row[10]
            dict[KEYS.TIME] = row[11]
            dict[KEYS.RULEID] = row[12]
            ret.append(dict)
        cur.close()
        return ret

    def deleteViolation(self, carid, ruleid, time):
        cur = self.con.cursor()
        command = "update violations set cleared = true " \
                  "where car = " + str(carid) + " and rule = " + str(ruleid) + " and time = " + str(time)
        rowcount = cur.execute(command).rowcount
        print("Deleted " + str(rowcount) + " rows")
        cur.close()
        self.con.commit()

    def getCamDetails(self, cam_id):
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

    def deleteAllCars(self):
        commad = "delete from cars"
        cur = self.con.cursor()
        cur.execute(commad)
        cur.close()
        self.con.commit()

    def deleteAllViolations(self):
        commad = "delete from violations"
        cur = self.con.cursor()
        cur.execute(commad)
        cur.close()
        self.con.commit()

    def getCamList(self, group):
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

    def getCamGroupList(self):
        command = "select name from camera_group"
        cur = self.con.cursor()
        cur.execute(command)
        rows = cur.fetchall()
        ret = [row[0] for row in rows]
        cur.close()
        return ret

    def clearCamLog(self):
        command = "update violations set cleared = true"
        cur = self.con.cursor()
        cur.execute(command)
        cur.close()
        self.con.commit()

    def convertTimeToDB(self, time):
        pass

    def convertTimeToGUI(self, time):
        pass
