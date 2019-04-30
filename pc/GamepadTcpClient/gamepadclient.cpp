#include "gamepadclient.h"

GamepadClient::GamepadClient(QString adress, int port):hostName(adress), hostPort(port)
{

}

GamepadClient::~GamepadClient()
{
   if(stateVar == 0)pTcpSocket->disconnectFromHost();
}

void GamepadClient::connectToHost()
{
    auto gamepads = QGamepadManager::instance()->connectedGamepads();

    if (!gamepads.isEmpty()) {
        stateVar = 0;

        gamepad = new QGamepad(*gamepads.begin(), this);

        pTcpSocket = new QTcpSocket(this);
        pTcpSocket->connectToHost(hostName, hostPort);

        connect(pTcpSocket, SIGNAL(connected()), this,SLOT(connectedToHost()));
        connect(this, SIGNAL(finished()),this, SLOT(threadFinished()));

        timer = new QTimer();
        timer->setInterval(20);
        connect(timer, SIGNAL(timeout()), this, SLOT(updateTime()));
        timer->start();
    }else{
        emit state(1);
        stateVar = 1;
    }
}

void GamepadClient::connectedToHost()
{
    stateVar = 0;
    emit state(0);
}

int GamepadClient::mapRange(int x, int in_min, int in_max, int out_min, int out_max)
{
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void GamepadClient::updateTime()
{
    buffer.clear();
    quint8 LX = mapRange(100*(gamepad->axisLeftX()),-100,100,0,255);
    quint8 LY = mapRange(100*(gamepad->axisLeftY()),-100,100,0,255);
    quint8 RX = mapRange(100*(gamepad->axisRightX()),-100,100,0,255);
    quint8 RY = mapRange(100*(gamepad->axisRightY()),-100,100,0,255);
    quint8 A  = gamepad->buttonA();
    quint8 B  = gamepad->buttonB();
    quint8 X  = gamepad->buttonX();
    quint8 Y  = gamepad->buttonY();
    quint8 BU = gamepad->buttonUp();
    quint8 BD = gamepad->buttonDown();
    quint8 BL = gamepad->buttonLeft();
    quint8 BR = gamepad->buttonRight();
    quint8 L2 = mapRange(100*(gamepad->buttonL2()),0,100,0,255);
    quint8 R2 = mapRange(100*(gamepad->buttonR2()),0,100,0,255);

    buffer.append(LX);
    buffer.append(LY);
    buffer.append(RX);
    buffer.append(RY);
    buffer.append(X);
    buffer.append(Y);
    buffer.append(B);
    buffer.append(A);
    buffer.append(BL);
    buffer.append(BU);
    buffer.append(BR);
    buffer.append(BD);
    buffer.append(L2);
    buffer.append(R2);
//    qDebug() <<L2;
//    qDebug() << R2;

    pTcpSocket->write(buffer);
}

void GamepadClient::threadFinished()
{
    pTcpSocket->disconnectFromHost();
    qDebug()<<"f";
}
