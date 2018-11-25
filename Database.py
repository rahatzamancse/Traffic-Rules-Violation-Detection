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

    def getUnclearedViolationsFromCam(self, cam):
        cur = self.con.cursor()
        command = "SELECT camera.location, cars.id, cars.color, cars.first_sighted, cars.license_image, " \
                  " cars.license_number, cars.car_image, cars.num_rules_broken, cars.owner," \
                  " rules.name, rules.fine, violations.time, rules.id" \
                  " FROM violations, rules, cars, camera" \
                  " where violations.camera = '" + str(cam) + \
                  "' and rules.id = violations.rule" \
                  " and cars.id = violations.car" \
                  " and violations.cleared = false"
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

    def deleteViolation(self, carid, ruleid, time):
        cur = self.con.cursor()
        # command = "delete from violations " \
        #           "where car = " + str(carid) + " and rule = " + str(ruleid) + " and time = " + str(time)
        command = "update violations set cleared = true " \
                  "where car = " + str(carid) + " and rule = " + str(ruleid) + " and time = " + str(time)
        # print(command)
        rowcount = cur.execute(command).rowcount
        print("Deleted " + str(rowcount) + " rows")
        cur.close()
        self.con.commit()

    def getCamViolationsCount(self, cam_id):
        command = "select count(*) from violations where camera = '" + str(cam_id) + "'"
        cur = self.con.cursor()
        count = cur.execute(command).fetchall()[0][0]
        command = "select location from camera where id = '" + str(cam_id) + "'"
        location = cur.execute(command).fetchall()[0][0]
        cur.close()
        return count, location


    def getCamList(self):
        command = "select id, location from camera"
        cur = self.con.cursor()
        cur.execute(command)
        rows = cur.fetchall()
        ret = []
        for row in rows:
            ret.append((row[0], row[1]))
        cur.close()
        return ret


    def clearCamLog(self):
        command = "update violations set cleared = true"
        cur = self.con.cursor()
        cur.execute(command)
        cur.close()
        self.con.commit()
