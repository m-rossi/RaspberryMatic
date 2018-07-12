#!/bin/sh

echo -ne "Content-Type: text/html; charset=iso-8859-1\r\n\r\n"

if [ -f /tmp/.runningFirmwareUpdate ]; then
  echo "Displaying running firmware update output:<br/>"
  echo "==========================================<br/>"

  [ -f /tmp/fwinstall.pid ] && kill $(cat /tmp/fwinstall.pid)
  /usr/bin/tail -F /tmp/fwinstall.log &
  echo $! >/tmp/fwinstall.pid
  wait $!

  echo "<br/>==========================================<br/>"
  echo "Browser closed connection.<br/>"
  exit 0
fi

cat <<EOF
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
    <meta http-equiv="expires" content="0">
    <link rel="stylesheet" type="text/css" href="css/index.css" />

    <title>CCU Recovery System</title>


  </head>
  <body id="body" bgcolor="#cccccc" text="#000000">
    <div id="webuilaoder_background">
      <div><img style="float: left; margin:10px; position: fixed;" src="img/homematic_logo_small.png"/></div>
      <div style="text-align: center;"><h1>CCU Recovery System</h1></div>
      <hr noshade size="4" align="left" color="white">
    </div>


    <table name="mainMenu" align="center">
      <tr>
        <td><div><input id="btnBack" style="display: none;" class="NavButton" type="button" onclick="reloadPage();" value="Back"></div></td>
      </tr>

      <tr>
        <td><div><input id="btnRecoveryUpdate" class="NavButton" type="button" onclick="showRecoveryUpdate();" value="Recovery/Update File"></div></td>
      </tr>

      <tr>
        <td><div><input id="btnRestoreBackupConfig" class="NavButton" type="button" onclick="showRestoreBackupConfig();" value="Create Backup"></div></td>
      </tr>
      <tr><td><hr noshade size="4" color="white"></td></tr>
    </table>

    <table name="mainMenu" align="center">
      <tr>
        <td id="tdRestoreBackupConfig" style="display: none;">
          <form name="bakUpload" action="cgi-bin/restore_backup.cgi" method="post" enctype="multipart/form-data">
            <p style="text-align: center">Backup Configuration</p>
              <div name='wrapper_'>
                <!-- <div>Security Key (optional): <input type="text" id="seckey" name="seckey"></div><br/> -->
                <!-- <div>Backup File: <input type="file" name="Datei" ></div> -->
              </div>
              <!-- <input class="NavButton" type="submit" value="Restore Backup" >-->
            <p style="text-align: center"><input class="NavButton" type="button" onclick="window.location.href = 'cgi-bin/create_backup.cgi';" value="Create Backup"></p>

          </form>
        </td>
      </tr>
      <tr align="center">
        <td id="tdRecoveryUpdate" style="display: none;">
          <form name="frmUpload" action="cgi-bin/firmware_update.cgi" method="post" enctype="multipart/form-data">
            <p>Recovery/Update File
              <div name='wrapper_'>
                <input type="file" name="Datei" ><br/><br/>
              </div>
              <br/>
              <input class="NavButton" type="submit" value="Start Recovery/Update" >
            </p>
          </form>
        </td>
      </tr>

    </table>


    <table name="mainMenu" id="tblBtnPanel" align="center">
      <tr>
        <td><div><input class="NavButton" type="button" onclick="confirmAction(0, this.value);" value="Factory Reset"></div></td>
      </tr>
      <tr>
        <td><div><input class="NavButton" type="button" onclick="confirmAction(1,this.value);" value="Reset Network Settings"></div></td>
      </tr>
      <tr><td><hr noshade size="4" color="white"></td></tr>
      <tr>
        <td><div><input class="NavButton" type="button" onclick="window.location.href = 'cgi-bin/safemode_boot.cgi';" value="Safe Mode Reboot"></div></td>
      </tr>
      <tr>
        <td><div><input class="NavButton" type="button" onclick="window.location.href = 'cgi-bin/normal_boot.cgi';" value="Normal Reboot"></div></td>
      </tr>
      <tr><td><hr noshade size="4" color="white"></td></tr>
    </table>

    <table name="mainMenu" id="btnInfoPanel" align="center">
      <tr>
        <td colspan="2">
          <input class="NavButton" type="button" onclick="showInfoPanel();" value="Info">
        </td>
      </tr>
    </table>

    <table name="mainMenu" align="center">
      <tr>
        <td>
          <p id="infoPanel" class="infoPanel" style="color:lightgrey; display: none;">
            recoveryfs: $(cat /VERSION | grep "VERSION=" | cut -f2 -d=)<br/>
            bootfs: $(cat /bootfs/VERSION | grep "VERSION=" | cut -f2 -d=)<br/>
            rootfs: $(cat /rootfs/VERSION | grep "VERSION=" | cut -f2 -d=)
          </p>
        </td>
      </tr>
    </table>

    <table id="confirmAction" align="center" style="visibility: hidden;">
      <tr>
        <td>
          <h1  style="color:lightgrey; text-align: center;">
            <div id="confirmActionText"></div>
          </h1>
        </td>
      </tr>

      <tr>
        <td style="text-align:center;">
          <input class="NavButton" type="button" onclick="reloadPage();" value="NO" style="margin-right:5em; " >
          <input id="btnConfirmYes" class="NavButton" type="button" value="YES">
        </td>
      </tr>

    </table>


    <script type="text/javascript">
      var elmBtnRestoreBackupConfig = document.getElementById("btnRestoreBackupConfig"),
        elmBtnRecoveryUpdate = document.getElementById("btnRecoveryUpdate"),
        elmTDRecoveryUpdate = document.getElementById("tdRecoveryUpdate"),
        elmTDRestoreBackupConfig = document.getElementById("tdRestoreBackupConfig"),
        elmTblBtnPanel = document.getElementById("tblBtnPanel"),
        elmBtnBack = document.getElementById("btnBack"),
        btnInfoPanel = document.getElementById("btnInfoPanel"),
        elmInfoPanel = document.getElementById("infoPanel"),
        elmsMainMenu = document.getElementsByName("mainMenu"),
        elmConfirmAction = document.getElementById("confirmAction"),
        elmConfirmActionText = document.getElementById("confirmActionText"),
        elmBtnConfirmYes = document.getElementById("btnConfirmYes");

      function reloadPage() {
        window.location.reload();
      }

      function showOnlyRelevantElems() {
        elmBtnRestoreBackupConfig.style.display = "none";
        elmBtnRecoveryUpdate.style.display = "none";
        elmTblBtnPanel.style.display = "none";
        btnInfoPanel.style.display = "none";
        elmInfoPanel.style.display = "none";
        elmBtnBack.style.display = "block";
      }

      function showRecoveryUpdate() {
        showOnlyRelevantElems();
        elmTDRecoveryUpdate.style.display = "block";
        elmTDRestoreBackupConfig.style.display = "none";
      }

      function showRestoreBackupConfig() {
        showOnlyRelevantElems();
        elmTDRecoveryUpdate.style.display = "none";
        elmTDRestoreBackupConfig.style.display = "block";
      }

      function showInfoPanel () {
        elmInfoPanel.style.display = elmInfoPanel.style.display == "none" ? "block" : "none";
      }

      function confirmAction(id, action) {
        console.log(action);
        showConfirmAction(id, action);
      }

      function showMainMenu() {
        elmConfirmAction.style.visibility = "hidden";

        for (var i in elmsMainMenu) {
          if (typeof elmsMainMenu[i] == "object") {
            elmsMainMenu[i].style.display = "block";
          }
        }
      }

      function showConfirmAction(id, action) {

        elmConfirmAction.style.visibility = "visible";
        result = false;
        switch (id) {
          case 0:
            elmConfirmActionText.innerHTML = "Do you really want to perform a factory reset?";
            elmBtnConfirmYes.onclick = function () {
               window.location.href = 'cgi-bin/factory_reset.cgi';
             };
             break;
          case 1:
            elmConfirmActionText.innerHTML = "Do you really want to reset the network settings?";
            elmBtnConfirmYes.onclick = function () {
              window.location.href = 'cgi-bin/network_reset.cgi';
             };
            break;
        }
        for (var i in elmsMainMenu) {
          if (typeof elmsMainMenu[i] == "object") {
            elmsMainMenu[i].style.display = "none";
          }
        }
      }

    </script>

  </body>
</html>
EOF