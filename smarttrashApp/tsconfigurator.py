# -*- coding: utf-8 -*-
import codecs
from configparser import ConfigParser

import os


class TSConfigurator(object):
    __ConfigurationFile = None  # path+name of config file
    __ConfigLoadingSuccess = False  # initial

    # Wifi
    __WIFI_SSID = ""
    __WIFI_PASSWORD = ""

    # Kaufland App Integration
    __KAppToken = ""  # permanent token for user account
    __KAppList = ""  # permanent token for user account
    __KAPPKeycloakToken_URI = ""
    __KAPPKeycloak_URI = ""
    __KAPPKeycloak_Client_ID = ""
    __KAPPKeycloak_CLIENT_SECRET = ""
    __KAPPBackend_Base = ""
    __KAPPBackend_API = ""
    __KAPPBackend_Subscription = ""

    # TrashScan Settings
    __MotionSensorDistance = 15  # in which distance should motions be detected?
    __SpeakerModeOn = False  # is a speaker attached and should speak?
    __UploadMode = 1  # upload to K-App directly (1) oder to local list first (2)?

    # OPTIONS
    __OPT_SECTION_INTEGRATION = "kaufland_app_integration"
    __OPT_SECTION_SETTINGS = "trashscan_settings"
    __OPT_SECTION_WIFI = "wifi"

    __OPT_K_APP_TOKEN = "k_app_token"
    __OPT_K_APP_LIST = "k_app_list"
    __OPT_K_APP_KEYCLOAK_TOKEN_URI = "k_app_keycloak_token_uri"
    __OPT_K_APP_KEYCLOAK_URI = "k_app_keycloak_uri"
    __OPT_K_APP_KEYCLOAK_CLIENT_ID = "k_app_keycloak_client_id"
    __OPT_K_APP_KEYCLOAK_CLIENT_SECRET = "k_app_keycloak_client_secret"
    __OPT_K_APP_BACKEND_BASE = "k_app_backend_base"
    __OPT_K_APP_BACKEND_API = "k_app_backend_api"
    __OPT_K_APP_BACKEND_SUBSCRIPTION = "k_app_backend_subscription"

    __OPT_MOTION_SENSOR_DISTANCE = "motion_sensor_distance"
    __OPT_SPEAKER_MODE_ON = "speaker_mode_on"
    __OPT_UPLOAD_MODE = "upload_mode"

    __OPT_WIFI_PASSWORD = "wifi_password"
    __OPT_WIFI_SSID = "wifi_ssid"

    def __init__(self, cfgfile=None):
        self.__ConfigurationFile = cfgfile
        self.__ConfigLoadingSuccess = False

    def readConfiguration(self):
        if not os.path.isfile(self.__ConfigurationFile):
            print("default")
            self.__loadDefault()
        else:
            config = ConfigParser()
            config.read(self.__ConfigurationFile, "utf8")
            self.__KAppToken = config.get(self.__OPT_SECTION_INTEGRATION, self.__OPT_K_APP_TOKEN)
            self.__KAppList = config.get(self.__OPT_SECTION_INTEGRATION, self.__OPT_K_APP_LIST)

            self.__KAPPKeycloakToken_URI = config.get(self.__OPT_SECTION_INTEGRATION,
                                                      self.__OPT_K_APP_KEYCLOAK_TOKEN_URI)
            self.__KAPPKeycloak_URI = config.get(self.__OPT_SECTION_INTEGRATION,
                                                 self.__OPT_K_APP_KEYCLOAK_URI)
            self.__KAPPKeycloak_Client_ID = config.get(self.__OPT_SECTION_INTEGRATION,
                                                       self.__OPT_K_APP_KEYCLOAK_CLIENT_ID)
            self.__KAPPKeycloak_CLIENT_SECRET = config.get(self.__OPT_SECTION_INTEGRATION,
                                                           self.__OPT_K_APP_KEYCLOAK_CLIENT_SECRET)
            self.__KAPPBackend_Base = config.get(self.__OPT_SECTION_INTEGRATION, self.__OPT_K_APP_BACKEND_BASE)
            self.__KAPPBackend_API = config.get(self.__OPT_SECTION_INTEGRATION, self.__OPT_K_APP_BACKEND_API)
            self.__KAPPBackend_Subscription = config.get(self.__OPT_SECTION_INTEGRATION,
                                                         self.__OPT_K_APP_BACKEND_SUBSCRIPTION)

            self.__MotionSensorDistance = config.getint(self.__OPT_SECTION_SETTINGS,
                                                        self.__OPT_MOTION_SENSOR_DISTANCE)
            self.__SpeakerModeOn = config.getboolean(self.__OPT_SECTION_SETTINGS, self.__OPT_SPEAKER_MODE_ON)
            self.__UploadMode = config.getint(self.__OPT_SECTION_SETTINGS, self.__OPT_UPLOAD_MODE)

            self.__WIFI_SSID = config.get(self.__OPT_SECTION_WIFI, self.__OPT_WIFI_SSID)
            self.__WIFI_PASSWORD = config.get(self.__OPT_SECTION_WIFI, self.__OPT_WIFI_PASSWORD)

            self.__ConfigLoadingSuccess = True

    def writeConfiguration(self):
        if self.__ConfigurationFile is not None:
            cfgfile = codecs.open(self.__ConfigurationFile, "w", "utf8")
            config = ConfigParser()

            config.add_section(self.__OPT_SECTION_INTEGRATION)
            config.set(self.__OPT_SECTION_INTEGRATION, self.__OPT_K_APP_TOKEN, self.getKAppToken())
            config.set(self.__OPT_SECTION_INTEGRATION, self.__OPT_K_APP_LIST, self.getKAppList())
            config.set(self.__OPT_SECTION_INTEGRATION, self.__OPT_K_APP_KEYCLOAK_TOKEN_URI, self.getKAppToken_URI())
            config.set(self.__OPT_SECTION_INTEGRATION, self.__OPT_K_APP_KEYCLOAK_URI, self.getKAppKeycloak_URI())
            config.set(self.__OPT_SECTION_INTEGRATION, self.__OPT_K_APP_KEYCLOAK_CLIENT_ID,
                       self.getKAppKeycloak_Client_ID())
            config.set(self.__OPT_SECTION_INTEGRATION, self.__OPT_K_APP_KEYCLOAK_CLIENT_SECRET,
                       self.getKAppKeycloak_Client_SECRET())
            config.set(self.__OPT_SECTION_INTEGRATION, self.__OPT_K_APP_BACKEND_BASE, self.getKAppBackend_Base())
            config.set(self.__OPT_SECTION_INTEGRATION, self.__OPT_K_APP_BACKEND_API, self.getKAppBackend_API())
            config.set(self.__OPT_SECTION_INTEGRATION, self.__OPT_K_APP_BACKEND_SUBSCRIPTION,
                       self.getKAppBackend_Subscription())

            config.add_section(self.__OPT_SECTION_SETTINGS)
            config.set(self.__OPT_SECTION_SETTINGS, self.__OPT_MOTION_SENSOR_DISTANCE,
                       str(self.getMotionSensorDistance()))
            config.set(self.__OPT_SECTION_SETTINGS, self.__OPT_SPEAKER_MODE_ON, str(self.isSpeakerModeOn()))
            config.set(self.__OPT_SECTION_SETTINGS, self.__OPT_UPLOAD_MODE, str(self.getUploadMode()))

            config.add_section(self.__OPT_SECTION_WIFI)
            config.set(self.__OPT_SECTION_WIFI, self.__OPT_WIFI_SSID, self.getWifiSSID())
            config.set(self.__OPT_SECTION_WIFI, self.__OPT_WIFI_PASSWORD, self.getWifiPassword())

            config.write(cfgfile)
            cfgfile.close()

    def __loadDefault(self):
        self.__KAppToken = ""
        self.__MotionSensorDistance = 15
        self.__SpeakerModeOn = False
        self.__UploadMode = 1
        self.__KAPPKeycloakToken_URI = ""
        self.__KAPPKeycloak_Client_ID = ""
        self.__KAPPBackend_Base = ""
        self.__KAPPBackend_Subscription = ""

    def getMotionSensorDistance(self):
        return self.__MotionSensorDistance

    def isSpeakerModeOn(self):
        return self.__SpeakerModeOn

    def getKAppToken(self):
        return self.__KAppToken

    def getKAppList(self):
        return self.__KAppList

    def getKAppToken_URI(self):
        return self.__KAPPKeycloakToken_URI

    def getKAppKeycloak_URI(self):
        return self.__KAPPKeycloak_URI

    def getKAppKeycloak_Client_ID(self):
        return self.__KAPPKeycloak_Client_ID

    def getKAppKeycloak_Client_SECRET(self):
        return self.__KAPPKeycloak_CLIENT_SECRET

    def getKAppBackend_Base(self):
        return self.__KAPPBackend_Base

    def getKAppBackend_API(self):
        return self.__KAPPBackend_API

    def getKAppBackend_Subscription(self):
        return self.__KAPPBackend_Subscription

    def getUploadMode(self):
        return self.__UploadMode

    def isConfigLoadingSuccess(self):
        return self.__ConfigLoadingSuccess

    def setKAppList(self, list: str):
        self.__KAppList = list
        self.writeConfiguration()

    def setKAppToken(self, token: str):
        self.__KAppToken = token
        self.writeConfiguration()

    def getWifiSSID(self):
        return self.__WIFI_SSID

    def getWifiPassword(self):
        return self.__WIFI_PASSWORD

    def setWifiSSID(self, ssid):
        self.__WIFI_SSID = ssid
        self.writeConfiguration()

    def setWifiPassword(self, password):
        self.__WIFI_PASSWORD = password
        self.writeConfiguration()

    def setMotionSensorDistance(self, distance):
        self.__MotionSensorDistance = distance
        self.writeConfiguration()

    def setSpeakerMode(self, speakerMode):
        self.__SpeakerModeOn = speakerMode
        self.writeConfiguration()

    def setUploadMode(self, uploadMode):
        self.__UploadMode = uploadMode
        self.writeConfiguration()
