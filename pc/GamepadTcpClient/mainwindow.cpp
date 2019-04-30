#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    this->setFixedSize(225,142);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_connectBtn_clicked()
{
   QThread* thread = new QThread;

   if(clicked == true) delete gmpad;

   gmpad = new GamepadClient(ui->hostAdress->text(), ui->hostPort->text().toInt());

   gmpad->moveToThread(thread);

   connect(thread, SIGNAL(started()), gmpad, SLOT(connectToHost()));
   connect(thread,SIGNAL(finished()),gmpad, SLOT(threadFinished()));
   connect(gmpad, SIGNAL(state(int)),this,SLOT(processState(int)));

   thread->start();
   clicked = true;
}

void MainWindow::processState(int st)
{
    switch (st) {
    case 0:
        ui->statusLabel->setText("Соединение установлено");
        break;
    case 1:
        ui->statusLabel->setText("Геймпад не обнаружен");
        break;
    default:
        break;
    }
}
