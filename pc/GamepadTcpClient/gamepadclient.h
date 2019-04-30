#ifndef GAMEPADCLIENT_H
#define GAMEPADCLIENT_H

#include <QObject>
#include <QDebug>
#include <QTcpSocket>
#include <QtGamepad/QGamepad>
#include <QtGamepad/QGamepadManager>
#include <QTimer>
#include <iostream>

class GamepadClient : public QObject
{
    Q_OBJECT
public:
    explicit GamepadClient(QString,int);
    ~GamepadClient();
    int mapRange(int x, int in_min, int in_max, int out_min, int out_max);

signals:
    void state(int);

public slots:
    void updateTime();
    void threadFinished();
    void connectToHost();
    void connectedToHost();

private:
    QTcpSocket* pTcpSocket;
    QGamepad *gamepad;
    QTimer *timer;
    QByteArray buffer;
    QString hostName;
    int hostPort, stateVar = 0;
};

#endif // GAMEPADCLIENT_H
