#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QThread>
#include <gamepadclient.h>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private slots:
    void on_connectBtn_clicked();
    void processState(int);

private:
    Ui::MainWindow *ui;
    GamepadClient *gmpad;
    bool clicked = false;
};

#endif // MAINWINDOW_H
