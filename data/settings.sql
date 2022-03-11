/*
 Navicat Premium Data Transfer

 Source Server         : bot_tuenvio
 Source Server Type    : SQLite
 Source Server Version : 3021000
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3021000
 File Encoding         : 65001

 Date: 24/07/2020 08:44:59
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for settings
-- ----------------------------
DROP TABLE IF EXISTS "settings";
CREATE TABLE "settings" (
  "id" INTEGER NOT NULL,
  "name" VARCHAR(255),
  "code" VARCHAR(255),
  "setting_type" VARCHAR(255),
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Records of settings
-- ----------------------------
INSERT INTO "settings" VALUES (1, 'notificaciones', 'notfy', 'alert');


PRAGMA foreign_keys = true;

