# air-quality-measurement-with-Raspberry-Pi.
Merhaba arkadaşlar

air quality-measurement with Raspberry-Pi.4 başlıklı projemiz, Marmara Üniversitesi Elektrik ve Elektronik Mühendisliği lisansüstü Gömülü Sistemler ve Mobil Uygulamalar ders doğrultusunda Dr.Öğr.Üyesi SERKAN AYDIN gözetiminde gerçekleştirilmiştir. Projemizin amacı kapalı ortamlarda hava kalitesinin bileşenlerini (sıcaklık, nem, LPG, CO ve duman) ölçen sensörlerden toplanan veriler, Raspberry pi yardımıyla alınır ve Wİ-Fİ aracıyla  Thingspeak ortamına aktarılarak grafiksel olarak izlenmesini sağlamış olur. Projenin doğru bir şekilde çalışması için üstteki wiki kısmına tıklayarak donanım ve yazılım hakkında verilen bilgiler dikkate alınarak gerçekleştirilmelidir.

![izlemesistemi](https://github.com/rohullah12344/air-quality-measurement-with-Raspberry-Pi.4/blob/main/izlemesistemi.png)
 IOT tabanlı Hava Kalite izleme sistemi mimarisi

# air-quality-measurement-with-Raspberry-Pi.
## Projeninin Amacı
projemizde Raspberry Pi 4 ile iç ortamlarda sıcaklık, nem, LPG, CO ve duman gibi hava kalitesi bileşenlerini ölçen sensör verileri, iot tabanlı platform (Thingspeak) ortamına aktırılması ve Thingspeak ortamında ilgili bileşenlerin deşiğimi gerçek zamanlı olarak izlenmesi hedeflemektedir. Amaçlanan projenin mermisi şekil 1 de verilmiştir. Burada veriler, sensör platformundan Raspberry pi 4 kart vasistasıyla alınmakladır ve bir internet protokol yardımıyla wifi üzerine Thingspeak ortamına aktarılmaktadır.
![ama%C3%A7lanan%20sistem](https://github.com/rohullah12344/air-quality-measurement-with-Raspberry-Pi/blob/main/ama%C3%A7lanan%20sistem.png)
## Donanım Hazırlığı:
Projenin başarıl bir şekilde çalışması aşağıdaki elemanların kullanımı haydalanmaktadır.  
* Raspberry 4 B model.
* MQ2 gaz sensörü.
* DHT11 nem ve sıcaklık sensörü.
* MCP3008 ADC entegresi.
* Bi-directional logic level converter.
* 2 tane 10k direnci Kablolar ve bread board 

![gerekliaygitlar](https://github.com/rohullah12344/air-quality-measurement-with-Raspberry-Pi/blob/main/gerekliaygitlar.png).

Şekil 2: a. DHT11 sensörü, b. MQ2 sensörü c. seviyesi dönüştürücü (TTL), d. MCP3008, e. Raspberry Pi.

DHT11 sensör sayısal bir sensördür bu sensörü kullanarak oramdaki nem ve sıcaklık değişimi Raspberry pi ile kolay bir şekilde ölçülebilmektedir. MQ2 gaz sensörü ise yapsındı analog ve dijital çıkışları bulundurmaktadır. Eğer ortamdaki sadece gazların varlığın algılanmak istenirse bu sensörün dijital çıkışnı (DO) kullanımı yeterli olacak, ancak havadaki farklı gazların değişimi ölçmek istendiğinde bu sensörün analog çıkışında yaranmak gerekmektedir. MQ2 gaz sensörün farklı gazların için nasıl kullanabilirliği MQ2 dashette ve gazların varlığına bağlı olarak analog çıkış gerilim hesaplanması da hazırladığım PDF dosyasından okuyabilirsiniz.

Raspberry Pi'nin sadece dijital sinyalleri işleyebilir ve yorumlayabilir, kendi başına analog sinyalleri işleyememektedir, bunun için MQ 2 sensörden alınan analog verileri Raspberry Pi'nin tarafından yönetebilmesi için bir analogdan dijitale dönüştürücüye ihtiyacımız var. ADC olarak MCP3008 entegresini kullandık. Raspberry Pi, MCP3008 kullanarak analog sinyalleri yorumlayabilir. Sesörlerin ve MCP3008 beslemesi için Rapbeer pi 5v ten yaralandık 5v GPIO'lar için çok fazla bir voltaj olmasından 5V to 3.3 Bi direction logig dünüştürüsüyü kulandık.

Dervrenin kurmu şekilde verilmiştir.burada MQ 2 gaz sensörü ve DHT11 sensorun beslemsi Rasipbery 5v pinden sağlanmakdır .MCP2008 raspberry pi daha hızlı haberleşme ve veri aktarımı sağlayabilen SPI pinlere sırasıyla şu şekilde bağlanmıştır

* VDD (Pin 16) bunu 3.3V'a bağlayın,
* VREF (Pin 15) bunu 3.3V'a bağlayın
* AGND (Pin 14) bunu toprağa bağlayın
* CLK (Pin 13) bunu GPIO11'e (Pin 23/SCLK) bağlayın
* DOUT (Pin 12) bunu GPIO9'a (Pin 21/MISO) bağlayın
* DIN (Pin 11) bunu GPIO10'a (Pin 19/MOSI) bağlayın
* CS (Pin 10) bunu GPIO8'e (Pin 24/CE0) bağlayın
* DGND (Pin 9) bunu GROUND'a bağlayın.
    
 MCP3008 doğru şekilde bağlandıktan sonra port 0'ı TTL'nin RX0'ına bağlarız. Karşı tarafta, MQ2 sensörünün analog (A0) bağlı olan RX1 bulunur. Ayrıca Raspberry Pi'den (LV) 3.3V ve TTL'ye 5V (HV) bağlayın. Ayrıca gaz sensörünün VCC pinine 5V ve Raspberry Pi'den GND, TTL'nin LV ve HV tarafında GND'ye ve ayrıca MQ2'nin GND'sine gelir.
 
 ![devre%20kurumu](https://github.com/rohullah12344/air-quality-measurement-with-Raspberry-Pi/blob/main/devre%20kurumu.png) ![MCP3008%20Baglanti](https://github.com/rohullah12344/air-quality-measurement-with-Raspberry-Pi/blob/main/MCP3008%20Baglanti.png)
 
 ## Yazılımsal çalışmalar
 ### Thingspeak Hesabı Oluşturma
 
 Kod yazımına geçmeden önce Thingspeak hesabına ihtiyacımız var. Buradaki https://thingspeak.com/ bağlantıya tıklayarak Thingspeak platformuna geçiş yapıp bir hesap oluştururuz. Hesabı oluşturduktan sonra sisteme giriş yapıyoruz ve NEW Chnnel tıklayarak kanalımızı oluşturuyoruz.
 
![kanal](https://github.com/rohullah12344/air-quality-measurement-with-Raspberry-Pi/blob/main/kanal.png)
    
Kanalımıza isim vererek açıklama kısmında isteğe bağlı açıklama yapıyoruz. Filel kısmı, veri aktarmak istediğimiz kısımdır. Thingspeak ücretsiz sürümünü kullandığımız için yalnızca 8 parametreye izin verilir. Daha fazla parametremiz varsa, ücretli sürümü kullanarak field sayısını artırabiliriz. Field1, field2, field3, field4 ve field5 kısımları sırasıyla Sıcaklık, nem, LPG, CO ve duman verilerin aktarılması için ayarlıyoruz.

![alan](https://github.com/rohullah12344/air-quality-measurement-with-Raspberry-Pi/blob/main/alan.png)

En son olarak “API Keys” sekmesine tıklıyoruz, Thingspeak bize Thingspeak ortamına veri transferi için ‘'Write API key” ve Thingspeak platformundan diğer platformuna veri aktarımı için “Read API key” anahtarları veriyor. ''Write API key” kodlarda kullanmak üzere kopyalayıp kaydediyoruz

![api](https://github.com/rohullah12344/air-quality-measurement-with-Raspberry-Pi/blob/main/api.png)

 ### Kodlar
 MCP3008 entegresinin Raspberry pi ile haberleşmeyi sağlayan ve mq2 sensörden veri alımı ve işleyişiyle ile ilgili kodlar ve açıklamalar[Raspberry Pi Gas Sensor MQ](https://github.com/tutRPi/Raspberry-Pi-Gas-Sensor-MQ) çalışmadan ulaşılabilir. MQ 2 dosyasında hesaplayan gazlar dışında diğer gazların değişimi incelemek isteyenler [mq2 datasheette](https://www.google.com/searchq=mq2+datasheet+pdf&oq=mq2+da&aqs=chrome.2.69i57j69i59j0i22i30l3j69i60l3.9463j0j7&sourceid=chrome&ie=UTF-8) verilen log formundaki değişmi incelemek istediği gazın (x,y) konumu ve eğrinin eğimi [WebPlotDigitizer](https://automeris.io/WebPlotDigitizer/) kullanılarak bulabilir ve seçtiği gaza bağlı olarak kodları değiştirebilir.
 
