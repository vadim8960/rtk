/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.12.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralWidget;
    QLineEdit *hostAdress;
    QLineEdit *hostPort;
    QLabel *label;
    QLabel *label_2;
    QPushButton *connectBtn;
    QLabel *statusLabel;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(225, 142);
        QSizePolicy sizePolicy(QSizePolicy::Fixed, QSizePolicy::Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(MainWindow->sizePolicy().hasHeightForWidth());
        MainWindow->setSizePolicy(sizePolicy);
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        hostAdress = new QLineEdit(centralWidget);
        hostAdress->setObjectName(QString::fromUtf8("hostAdress"));
        hostAdress->setGeometry(QRect(10, 30, 131, 25));
        hostPort = new QLineEdit(centralWidget);
        hostPort->setObjectName(QString::fromUtf8("hostPort"));
        hostPort->setGeometry(QRect(160, 30, 51, 25));
        label = new QLabel(centralWidget);
        label->setObjectName(QString::fromUtf8("label"));
        label->setGeometry(QRect(10, 10, 141, 17));
        label_2 = new QLabel(centralWidget);
        label_2->setObjectName(QString::fromUtf8("label_2"));
        label_2->setGeometry(QRect(160, 10, 67, 17));
        connectBtn = new QPushButton(centralWidget);
        connectBtn->setObjectName(QString::fromUtf8("connectBtn"));
        connectBtn->setGeometry(QRect(10, 70, 201, 31));
        statusLabel = new QLabel(centralWidget);
        statusLabel->setObjectName(QString::fromUtf8("statusLabel"));
        statusLabel->setGeometry(QRect(10, 110, 201, 17));
        MainWindow->setCentralWidget(centralWidget);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "Gamepad TCP client", nullptr));
        hostAdress->setText(QApplication::translate("MainWindow", "192.168.0.20", nullptr));
        hostPort->setText(QApplication::translate("MainWindow", "9997", nullptr));
        label->setText(QApplication::translate("MainWindow", "\320\220\320\264\321\200\320\265\321\201 Raspberry Pi", nullptr));
        label_2->setText(QApplication::translate("MainWindow", "\320\237\320\276\321\200\321\202", nullptr));
        connectBtn->setText(QApplication::translate("MainWindow", "\320\237\320\276\320\264\320\272\320\273\321\216\321\207\320\270\321\202\321\214 \320\263\320\265\320\271\320\274\320\277\320\260\320\264", nullptr));
        statusLabel->setText(QString());
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
