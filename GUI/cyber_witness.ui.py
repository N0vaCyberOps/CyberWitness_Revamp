<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>600</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Cyber Witness</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <layout class="QVBoxLayout" name="mainLayout">
    <item>
     <widget class="QWidget" name="loginWidget">
      <layout class="QHBoxLayout" name="loginLayout">
       <item>
        <widget class="QLabel" name="usernameLabel">
         <property name="text">
          <string>Username:</string>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QLineEdit" name="usernameInput"/>
       </item>
       <item>
        <widget class="QLabel" name="passwordLabel">
         <property name="text">
          <string>Password:</string>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QLineEdit" name="passwordInput">
         <property name="echoMode">
          <enum>QLineEdit::Password</enum>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QPushButton" name="loginButton">
         <property name="text">
          <string>Login</string>
         </property>
        </widget>
       </item>
      </layout>
     </widget>
    </item>
    <item>
     <widget class="QTabWidget" name="mainTabs">
      <property name="visible">
       <bool>false</bool>
      </property>
      <widget class="QWidget" name="dashboardTab">
       <attribute name="title">
        <string>Dashboard</string>
       </attribute>
       <layout class="QVBoxLayout" name="dashboardLayout">
        <item>
         <widget class="QChartView" name="trafficChart"/>
        </item>
       </layout>
      </widget>
      <widget class="QWidget" name="alertsTab">
       <attribute name="title">
        <string>Alerts</string>
       </attribute>
       <layout class="QVBoxLayout" name="alertsLayout">
        <item>
         <widget class="QTableWidget" name="alertsTable">
          <column>
           <property name="text">
            <string>Timestamp</string>
           </property>
          </column>
          <column>
           <property name="text">
            <string>Severity</string>
           </property>
          </column>
          <column>
           <property name="text">
            <string>Description</string>
           </property>
          </column>
         </widget>
        </item>
       </layout>
      </widget>
      <widget class="QWidget" name="snifferTab">
       <attribute name="title">
        <string>Sniffer</string>
       </attribute>
       <layout class="QVBoxLayout" name="snifferLayout">
        <item>
         <layout class="QHBoxLayout" name="interfaceLayout">
          <item>
           <widget class="QLabel" name="interfaceLabel">
            <property name="text">
             <string>Interface:</string>
            </property>
           </widget>
          </item>
          <item>
           <widget class="QComboBox" name="interfaceCombo">
            <item>
             <property name="text">
              <string>eth0</string>
             </property>
            </item>
            <item>
             <property name="text">
              <string>wlan0</string>
             </property>
            </item>
           </widget>
          </item>
         </layout>
        </item>
        <item>
         <widget class="QPushButton" name="startSnifferButton">
          <property name="text">
           <string>Start Sniffer</string>
          </property>
         </widget>
        </item>
        <item>
         <widget class="QPushButton" name="stopSnifferButton">
          <property name="text">
           <string>Stop Sniffer</string>
          </property>
         </widget>
        </item>
        <item>
         <widget class="QPushButton" name="exportReportsButton">
          <property name="text">
           <string>Export Reports</string>
          </property>
         </widget>
        </item>
       </layout>
      </widget>
      <widget class="QWidget" name="usersTab">
       <attribute name="title">
        <string>Users</string>
       </attribute>
       <layout class="QVBoxLayout" name="usersLayout">
        <item>
         <widget class="QTableWidget" name="usersTable">
          <column>
           <property name="text">
            <string>Username</string>
           </property>
          </column>
          <column>
           <property name="text">
            <string>Role</string>
           </property>
          </column>
          <column>
           <property name="text">
            <string>Actions</string>
           </property>
          </column>
         </widget>
        </item>
        <item>
         <widget class="QPushButton" name="addUserButton">
          <property name="text">
           <string>Add User</string>
          </property>
         </widget>
        </item>
       </layout>
      </widget>
      <widget class="QWidget" name="configTab">
       <attribute name="title">
        <string>Config</string>
       </attribute>
       <layout class="QVBoxLayout" name="configLayout">
        <item>
         <layout class="QHBoxLayout" name="thresholdLayout">
          <item>
           <widget class="QLabel" name="thresholdLabel">
            <property name="text">
             <string>Alert Threshold:</string>
            </property>
           </widget>
          </item>
          <item>
           <widget class="QLineEdit" name="thresholdInput">
            <property name="text">
             <string>100</string>
            </property>
           </widget>
          </item>
         </layout>
        </item>
        <item>
         <layout class="QHBoxLayout" name="filterLayout">
          <item>
           <widget class="QLabel" name="filterLabel">
            <property name="text">
             <string>Filter:</string>
            </property>
           </widget>
          </item>
          <item>
           <widget class="QLineEdit" name="filterInput">
            <property name="text">
             <string>TCP/UDP</string>
            </property>
           </widget>
          </item>
         </layout>
        </item>
        <item>
         <widget class="QPushButton" name="saveConfigButton">
          <property name="text">
           <string>Save Config</string>
          </property>
         </widget>
        </item>
       </layout>
      </widget>
      <widget class="QWidget" name="kibanaTab">
       <attribute name="title">
        <string>Kibana</string>
       </attribute>
       <layout class="QVBoxLayout" name="kibanaLayout">
        <item>
         <widget class="QLabel" name="kibanaView">
          <property name="text">
           <string>Embedded Kibana Dashboard Placeholder</string>
          </property>
         </widget>
        </item>
       </layout>
      </widget>
     </widget>
    </item>
   </layout>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>