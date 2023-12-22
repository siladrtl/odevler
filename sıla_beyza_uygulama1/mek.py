import typing
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget,QMainWindow,QTableWidgetItem,QTableWidget,QHeaderView,QMessageBox,QPushButton,QLineEdit,QVBoxLayout
from PyQt5.QtGui import QPixmap,QIcon
from _mek import Ui_MainWindow
import sys
import sqlite3
conn= sqlite3.connect("meks.db")
cursor = conn.cursor()
conn.commit()

table = cursor.execute ("CREATE TABLE IF NOT EXISTS Sirkets (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,Marka TEXT , Adet TEXT , Fiyat TEXT , Tarih TEXT   , Depolama TEXT , Turu TEXT )")
conn.commit()



class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        
        self.setupUi(self)
        self.setWindowTitle('Sirket')
        self.label.setPixmap(QPixmap('logo (1).png'))
        self.pushButton_2.clicked.connect(self.kayit_ekle)
        self.pushButton.clicked.connect(self.kayit_listele)
        self.pushButton_3.clicked.connect(self.kayit_sil)
        self.kayit_listele() 
        


    def kayit_ekle(self):
        Marka = self.lineEdit.text()
        Adet = self.lineEdit_2.text()
        Fiyat = self.lineEdit_3.text()
        Tarih = self.lineEdit_4.text()
        Depolama = self.lineEdit_5.text()
        Turu = "tur"

        if self.radioButton.isChecked():
            Turu = "İthal"
        elif self.radioButton_2.isChecked():
            Turu="Yerel"
            


    
        ekle = "INSERT INTO Sirkets (Marka,Adet,Fiyat,Tarih,Depolama,Turu)VALUES(?,?,?,?,?,?)"
        cursor.execute(ekle, (Marka,Adet,Fiyat,Tarih,Depolama,Turu))
        conn.commit()
        self.kayit_listele()
        
        

   
   
    def kayit_listele(self):
        self.tableWidget.clear()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setHorizontalHeaderLabels(("ID","Marka","Adet","Fiyat","Tarih","Depolama","Turu"))
   
        sorgu = "SELECT * FROM Sirkets"
        # eklenenler =cursor.fetchall()
        cursor.execute(sorgu)


        for indexSatir,kayitNumarasi in enumerate(cursor):
            for indexSutun , kayitSutun in enumerate(kayitNumarasi):
                self.tableWidget.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSutun)))

    # def kayit_sil(self):  
    #     sil_mesaj =QMessageBox.question(self,"Silme onayı ","Silmek istediğinizden emin misiniz?",
    #     QMessageBox.Yes | QMessageBox.No)
       
  
    def kayit_sil(self):  
        sil_mesaj = QMessageBox.question(self, "Silme Onayı", "Silmek istediğinizden emin misiniz?",
                                         QMessageBox.Yes | QMessageBox.No)
       
        if sil_mesaj == QMessageBox.Yes:
            secilen_kayit = self.tableWidget.currentItem()

            sorgu = "DELETE FROM Sirkets WHERE ID = ?"
            try:
                cursor.execute(sorgu, (self.tableWidget.item(secilen_kayit.row(), 0).text(),))
                conn.commit()
                
                self.statusbar.showMessage("Kayıt başarıyla silindi")
            except Exception as error:
                self.statusbar.showMessage("Kayıt silinirken hata çıktı: " + str(error))
                conn.close()
            
            self.kayit_listele()
        


       
        
        

def app():
    app=QtWidgets.QApplication(sys.argv)
    win=Window()
    win.show()
    sys.exit(app.exec_())

app()
        
        
        




    