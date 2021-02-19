#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    m_client = new QMqttClient(this);
    m_client->setHostname("49.232.128.246");
    m_client->setPort(1883);

    connect(m_client, &QMqttClient::connected, this, [=]
    {
        m_client->subscribe(subTopic, 0);
    });

    connect(m_client, &QMqttClient::messageReceived, this, [=](const QByteArray &message, const QMqttTopicName &topic)
    {
        QString rectopic = topic.name();
        recMsg = message;
        if (QString::compare(recMsg, "Ra")==0)
        {
            if (Rv == 100)
            {
                Rv = 0;
            }
            else
            {
                Rv++;
            }
            ui->labRv->setText(QString::number(Rv));
        }
        else if (QString::compare(recMsg, "Rd")==0)
        {
            if (Rv == 0)
            {
                Rv = 100;
            }
            else
            {
                Rv--;
            }
            ui->labRv->setText(QString::number(Rv));
        }
        else if (QString::compare(recMsg, "Ga")==0)
        {
            if (Gv == 100)
            {
                Gv = 0;
            }
            else
            {
                Gv++;
            }
            ui->labGv->setText(QString::number(Gv));
        }
        else if (QString::compare(recMsg, "Gd")==0)
        {
            if (Gv == 0)
            {
                Gv = 100;
            }
            else
            {
                Gv--;
            }
            ui->labGv->setText(QString::number(Gv));
        }
        else if (QString::compare(recMsg, "Ba")==0)
        {
            if (Bv == 100)
            {
                Bv = 0;
            }
            else
            {
                Bv++;
            }
            ui->labBv->setText(QString::number(Bv));
        }
        else if (QString::compare(recMsg, "Bd")==0)
        {
            if (Bv == 0)
            {
                Bv = 100;
            }
            else
            {
                Bv--;
            }
            ui->labBv->setText(QString::number(Bv));
        }
    });
    m_client->connectToHost();
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_btnRd_clicked()
{
    if (Rv == 0)
    {
        Rv = 100;
    }
    else
    {
        Rv--;
    }
    ui->labRv->setText(QString::number(Rv));
    sendMsg = "Rd";
    m_client->publish(pubTopic, sendMsg.toUtf8());
}

void MainWindow::on_btnRa_clicked()
{
    if (Rv == 100)
    {
        Rv = 0;
    }
    else
    {
        Rv++;
    }
    ui->labRv->setText(QString::number(Rv));
    sendMsg = "Ra";
    m_client->publish(pubTopic, sendMsg.toUtf8());
}

void MainWindow::on_btnGd_clicked()
{
    if (Gv == 0)
    {
        Gv = 100;
    }
    else
    {
        Gv--;
    }
    ui->labGv->setText(QString::number(Gv));
    sendMsg = "Gd";
    m_client->publish(pubTopic, sendMsg.toUtf8());
}

void MainWindow::on_btnGa_clicked()
{
    if (Gv == 100)
    {
        Gv = 0;
    }
    else
    {
        Gv++;
    }
    ui->labGv->setText(QString::number(Gv));
    sendMsg = "Ga";
    m_client->publish(pubTopic, sendMsg.toUtf8());
}

void MainWindow::on_btnBd_clicked()
{
    if (Bv == 0)
    {
        Bv = 100;
    }
    else
    {
        Bv--;
    }
    ui->labBv->setText(QString::number(Bv));
    sendMsg = "Bd";
    m_client->publish(pubTopic, sendMsg.toUtf8());
}

void MainWindow::on_btnBa_clicked()
{
    if (Bv == 100)
    {
        Bv = 0;
    }
    else
    {
        Bv++;
    }
    ui->labBv->setText(QString::number(Bv));
    sendMsg = "Ba";
    m_client->publish(pubTopic, sendMsg.toUtf8());
}

