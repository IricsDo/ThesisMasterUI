#include <QGuiApplication>
#include <QQmlApplicationEngine>

#include <QIcon>
#include <QLocale>
#include <QPixmap>
#include <QTranslator>

int main(int argc, char *argv[])
{
    qputenv("QT_IM_MODULE", QByteArray("qtvirtualkeyboard"));

#if QT_VERSION < QT_VERSION_CHECK(6, 0, 0)
    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
#endif
    QGuiApplication app(argc, argv);

    app.setOrganizationName("Iric");
    app.setOrganizationDomain("iric.life1407@gmail.com");
    app.setApplicationName("Unmanned-Surveillance-Device-USD");
    app.setApplicationDisplayName("Unmanned-Surveillance-Device-USD");
    app.setDesktopFileName("Unmanned-Surveillance-Device-USD");
    app.setWindowIcon(QIcon(QPixmap(":/icons/ai_64.png")));

    QTranslator translator;
    const QStringList uiLanguages = QLocale::system().uiLanguages();
    for (const QString &locale : uiLanguages) {
        const QString baseName = "ThesisMasterUI_" + QLocale(locale).name();
        if (translator.load(":/i18n/" + baseName)) {
            app.installTranslator(&translator);
            break;
        }
    }

    QQmlApplicationEngine engine;
    const QUrl url(QStringLiteral("qrc:/main.qml"));
    QObject::connect(
        &engine,
        &QQmlApplicationEngine::objectCreated,
        &app,
        [url](QObject *obj, const QUrl &objUrl) {
            if (!obj && url == objUrl)
                QCoreApplication::exit(-1);
        },
        Qt::QueuedConnection);
    engine.load(url);

    return app.exec();
}
