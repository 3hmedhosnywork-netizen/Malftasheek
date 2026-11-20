# مرسال المواقع — نسخة إعادة البناء 1


- مشاركة رابط Google Maps إلى التطبيق أو لصقه يدويًا.
- تحديد بادئة الكود والرقم الأول يدويًا؛ يظل الحقلان فارغين عند أول تشغيل.
- إضافة المواقع بترقيم متتابع، مع حفظها على الجهاز.
- إرسال الكل إلى واتساب في رسالة واحدة، وكل موقع بتنسيق: الرابط ثم عدة أسطر فارغة ثم الكود.
- إعادة إرسال موقع منفرد دون تغيير ترتيبه أو حالة إرساله.
- زر مسح المكتمل يحذف العناصر التي تم تأكيد إرسالها فقط.
- قائمة مواقع صغيرة ومختصرة.

## النشر
ارفع كل ملفات هذا المجلد إلى جذر مستودع GitHub Pages (بدون رفع المجلد نفسه كطبقة إضافية). ثم Settings > Pages > Deploy from branch > main > /(root).

## ملاحظة مشاركة Maps
Share Target على Android/Chrome يعتمد على دعم النظام والمتصفح وكون التطبيق مثبتًا من Pages. إذا لم يظهر التطبيق ضمن قائمة مشاركة Google Maps، يمكن لصق الرابط داخل التطبيق يدويًا.


## V2 changes (Nov 19, 2026)
- Send-all now opens WhatsApp with one pending site per message, in list order.
- The send-all button label shows the next pending site code; after confirming a site sent, it points to the next pending site.
- Clear button is now “مسح الكل” and removes all saved sites, pending and sent, after confirmation.
- This version was checked for archive/file integrity; WhatsApp and Android share-target behavior still needs a real-device test.


## V5: pin-code extraction from Google Maps shares

The share handler now searches the human-readable share title/text (before any URL) for a code such as A111 or M68. If it finds one, it saves the shared Maps link under that exact code and blocks duplicate codes. If the share payload contains only a URL, the app leaves the link ready and asks the user to enter the pin code manually instead of inventing a sequential code. The share payload format varies by source app/Android; this extraction must be tested on the user device to confirm Google Maps includes the pin label.
