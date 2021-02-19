#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

#include "QtMqtt/qmqttclient.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

    QString subTopic = "ctrlpub";
    QString pubTopic = "ctrlsub";
    QString sendMsg;
    QString recMsg;

private slots:

    void on_btnRd_clicked();

    void on_btnRa_clicked();

    void on_btnGd_clicked();

    void on_btnGa_clicked();

    void on_btnBd_clicked();

    void on_btnBa_clicked();


private:
    Ui::MainWindow *ui;
    QMqttClient *m_client;
    int Rv = 0;
    int Gv = 0;
    int Bv = 0;
};
#endif // MAINWINDOW_H
