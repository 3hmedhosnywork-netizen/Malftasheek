from pathlib import Path

html = r'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>محدّث ملف التشييك</title>
<script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
<style>
:root{--bg:#f3f6fb;--card:#fff;--ink:#172033;--muted:#64748b;--accent:#155eef;--line:#dbe3ef;--good:#087443;--warn:#9a6700}
*{box-sizing:border-box}body{margin:0;background:var(--bg);font-family:system-ui,-apple-system,"Segoe UI",Tahoma,Arial,sans-serif;color:var(--ink)}
.wrap{max-width:920px;margin:auto;padding:20px 14px 40px}.hero{background:linear-gradient(135deg,#102a56,#155eef);color:#fff;padding:24px;border-radius:22px;margin-bottom:16px;box-shadow:0 12px 28px #123b7520}
h1{font-size:25px;margin:0 0 8px}.hero p{margin:0;line-height:1.8;color:#e5edff}.card{background:var(--card);padding:18px;border:1px solid var(--line);border-radius:18px;margin:14px 0;box-shadow:0 5px 16px #15284a08}
h2{font-size:18px;margin:0 0 12px}.step{display:inline-flex;background:#e8efff;color:#1749a3;border-radius:999px;padding:4px 10px;font-size:12px;font-weight:700;margin-bottom:8px}
label{display:block;font-weight:650;margin:10px 0 7px}input[type=file],select{width:100%;padding:12px;border:1px solid #cbd5e1;border-radius:12px;background:#fff;font:inherit}
button{border:0;border-radius:12px;padding:12px 16px;font:inherit;font-weight:700;cursor:pointer;background:var(--accent);color:#fff;margin-top:12px}button.secondary{background:#e8efff;color:#1749a3}button:disabled{opacity:.45;cursor:not-allowed}.hint{color:var(--muted);font-size:13px;line-height:1.8}.status{padding:12px;border-radius:12px;background:#f1f5f9;margin-top:12px;line-height:1.8;white-space:pre-wrap}.status.good{background:#e8f7ef;color:var(--good)}.status.warn{background:#fff6df;color:var(--warn)}
table{border-collapse:collapse;width:100%;margin-top:12px;font-size:14px}th,td{padding:10px;border-bottom:1px solid var(--line);text-align:right}th{background:#f8fafc}tr:last-child td{border-bottom:0}.table-wrap{overflow-x:auto}.radio{display:flex;gap:9px;align-items:flex-start;padding:12px;border:1px solid var(--line);border-radius:12px;margin:8px 0}.radio input{margin-top:5px}.radio small{display:block;color:var(--muted);margin-top:3px}.footer{font-size:12px;color:var(--muted);line-height:1.8;text-align:center;margin-top:18px}.hidden{display:none!important}
</style>
</head>
<body>
<div class="wrap">
  <header class="hero">
    <h1>محدّث ملف التشييك</h1>
    <p>ارفع الملف الأساسي ومحفظة اليوم، راجع المالك الأكثر تطابقًا، ثم نزّل نسخة محدّثة. الملفات تُعالَج داخل المتصفح ولا تُرسل إلى هذا الموقع.</p>
  </header>

  <section class="card">
    <span class="step">الخطوة ١</span><h2>رفع ملف التشييك الأساسي</h2>
    <label for="baseFile">ملف Excel الأساسي</label><input id="baseFile" type="file" accept=".xlsx,.xls,.xlsm">
    <div class="hint">اختَر الملف الذي يحتوي على اللوحات وأسماء الملاك. يفضّل أن يكون الصف الأول هو عناوين الأعمدة.</div>
    <div id="baseStatus" class="status">لم يتم اختيار ملف بعد.</div>
  </section>

  <section class="card">
    <span class="step">الخطوة ٢</span><h2>رفع محفظة اليوم</h2>
    <label for="portfolioFile">ملف المحفظة الجديدة</label><input id="portfolioFile" type="file" accept=".xlsx,.xls,.xlsm">
    <div class="hint">سيحاول الموقع اكتشاف أعمدة اللوحة واسم المالك تلقائيًا. راجع الاختيارات إذا لم يتعرف عليها بشكل صحيح.</div>
    <div id="columnOptions" class="hidden">
      <label for="baseSheet">ورقة التشييك الأساسية</label><select id="baseSheet"></select>
      <label for="portSheet">ورقة المحفظة</label><select id="portSheet"></select>
      <label for="basePlate">عمود اللوحة في الملف الأساسي</label><select id="basePlate"></select>
      <label for="baseOwner">عمود اسم المالك في الملف الأساسي</label><select id="baseOwner"></select>
      <label for="portPlate">عمود اللوحة في المحفظة الجديدة</label><select id="portPlate"></select>
      <button id="compareBtn">قارن اللوحات</button>
    </div>
    <div id="portfolioStatus" class="status">لم يتم اختيار ملف بعد.</div>
  </section>

  <section class="card hidden" id="resultsCard">
    <span class="step">الخطوة ٣</span><h2>نتيجة المقارنة واختيار المالك</h2>
    <div id="summary"></div>
    <div class="table-wrap" id="countsTable"></div>
    <label for="ownerChoice">اختَر المالك الذي تريد تحديث بياناته</label>
    <select id="ownerChoice"></select>
    <div class="hint">سيكون المالك صاحب أكبر عدد من التطابقات هو الاختيار الافتراضي، ويمكنك تغييره يدويًا.</div>
    <div class="status warn">تنبيه: التحديث يستبدل كل صفوف المالك المختار بصفوف المحفظة الجديدة. لا تُنقل اللوحات إلى مالك آخر تلقائيًا. راجع الاختيار قبل التنفيذ.</div>
    <button id="previewBtn">عرض ملخص التحديث</button>
    <div id="preview" class="hidden"></div>
    <button id="downloadBtn" class="hidden">تنزيل ملف التشييك المحدّث</button>
  </section>
  <div class="footer">نسخة تجريبية أولية. جرّبها على نسخة من ملفاتك أولًا، ولا تستخدمها كبديل عن الاحتفاظ بنسخة احتياطية.</div>
</div>

<script>
(() => {
 const $ = id => document.getElementById(id);
 let baseWB=null, portWB=null, baseRows=[], portRows=[], headers=[], portHeaders=[], ownerCounts=[], matchedOwner=null, outputWB=null, chosenBaseSheet='';
 const plateKeys=['اللوحة','اللوح','رقم اللوحة','لوحة','plate','plate number','registration','رقم'];
 const ownerKeys=['اسم المالك','المالك','الجهة','البنك','اسم البنك','owner','customer','client'];
 function norm(s){return String(s??'').trim().toLowerCase().replace(/[\s\-_./\\]+/g,'').replace(/[أإآ]/g,'ا').replace(/ة/g,'ه').replace(/[٠-٩]/g,d=>'٠١٢٣٤٥٦٧٨٩'.indexOf(d)).replace(/[۰-۹]/g,d=>'۰۱۲۳۴۵۶۷۸۹'.indexOf(d));}
 function plateNorm(v){return norm(v).replace(/[^a-z\u0600-\u06ff0-9]/g,'');}
 function guess(headers, keys, fallback=0){let best=-1,bestScore=0;headers.forEach((h,i)=>{let n=norm(h),score=0;keys.forEach(k=>{let nk=norm(k);if(n===nk)score+=5;else if(n.includes(nk)||nk.includes(n))score+=2});if(score>bestScore){bestScore=score;best=i}});return best>=0?best:fallback}
 function readFile(file){return new Promise((resolve,reject)=>{const r=new FileReader();r.onload=e=>{try{resolve(XLSX.read(e.target.result,{type:'array',cellDates:true}))}catch(err){reject(err)}};r.onerror=reject;r.readAsArrayBuffer(file)})}
 function sheetData(wb,name){const ws=wb.Sheets[name];const aoa=XLSX.utils.sheet_to_json(ws,{header:1,defval:'',raw:false});let hi=0,max=-1;for(let i=0;i<Math.min(aoa.length,15);i++){let filled=aoa[i].filter(x=>String(x).trim()!=='').length;if(filled>max){max=filled;hi=i}}const hs=(aoa[hi]||[]).map((h,i)=>String(h??'').trim()||`عمود ${i+1}`);const rows=aoa.slice(hi+1).filter(row=>row.some(v=>String(v??'').trim()!=='')).map(row=>{let o={};hs.forEach((h,i)=>o[h]=row[i]??'');return o});return {headers:hs,rows,headerRow:hi,aoa}}
 function fillSelect(id,opts,selected){const s=$(id);s.innerHTML='';opts.forEach((o,i)=>{const op=document.createElement('option');op.value=String(i);op.textContent=o;s.appendChild(op)});if(selected!==undefined&&selected>=0)s.value=String(selected)}
 function selectedSheet(id,wb){return wb.SheetNames[Number($(id).value)]}
 function setStatus(id,msg,kind=''){const el=$(id);el.textContent=msg;el.className='status'+(kind?' '+kind:'')}
 $('baseFile').addEventListener('change',async e=>{try{if(!e.target.files[0])return;baseWB=await readFile(e.target.files[0]);fillSelect('baseSheet',baseWB.SheetNames,0);loadColumnOptions();setStatus('baseStatus',`تم تحميل الملف: ${e.target.files[0].name}\nعدد أوراق العمل: ${baseWB.SheetNames.length}`,'good')}catch(err){setStatus('baseStatus','تعذّر قراءة الملف. تأكد أنه ملف Excel صالح.','warn')}});
 $('portfolioFile').addEventListener('change',async e=>{try{if(!e.target.files[0])return;portWB=await readFile(e.target.files[0]);fillSelect('portSheet',portWB.SheetNames,0);loadColumnOptions();setStatus('portfolioStatus',`تم تحميل الملف: ${e.target.files[0].name}\nعدد أوراق العمل: ${portWB.SheetNames.length}`,'good')}catch(err){setStatus('portfolioStatus','تعذّر قراءة الملف. تأكد أنه ملف Excel صالح.','warn')}});
 $('baseSheet').addEventListener('change',loadColumnOptions);$('portSheet').addEventListener('change',loadColumnOptions);
 function loadColumnOptions(){if(!baseWB||!portWB)return;const b=sheetData(baseWB,selectedSheet('baseSheet',baseWB));const p=sheetData(portWB,selectedSheet('portSheet',portWB));headers=b.headers;portHeaders=p.headers;fillSelect('basePlate',headers,guess(headers,plateKeys,0));fillSelect('baseOwner',headers,guess(headers,ownerKeys,Math.min(1,headers.length-1)));fillSelect('portPlate',portHeaders,guess(portHeaders,plateKeys,0));$('columnOptions').classList.remove('hidden');$('resultsCard').classList.add('hidden');}
 $('compareBtn').addEventListener('click',()=>{if(!baseWB||!portWB)return;try{chosenBaseSheet=selectedSheet('baseSheet',baseWB);const b=sheetData(baseWB,chosenBaseSheet),p=sheetData(portWB,selectedSheet('portSheet',portWB));headers=b.headers;portHeaders=p.headers;baseRows=b.rows;portRows=p.rows;const bp=headers[Number($('basePlate').value)],bo=headers[Number($('baseOwner').value)],pp=portHeaders[Number($('portPlate').value)];if(!bp||!bo||!pp)throw new Error('راجع أعمدة اللوحة والمالك.');const owners=new Map();const plateOwner=new Map();baseRows.forEach(r=>{let pl=plateNorm(r[bp]),owner=String(r[bo]??'').trim();if(pl&&owner){plateOwner.set(pl,owner);owners.set(owner,(owners.get(owner)||0)+0)}});const counts=new Map(),matchesByOwner=new Map();let unmatched=0,matched=0;portRows.forEach(r=>{const pl=plateNorm(r[pp]);if(!pl)return;const owner=plateOwner.get(pl);if(owner){matched++;counts.set(owner,(counts.get(owner)||0)+1);if(!matchesByOwner.has(owner))matchesByOwner.set(owner,[]);matchesByOwner.get(owner).push(r)}else unmatched++});ownerCounts=[...counts.entries()].sort((a,b)=>b[1]-a[1]);matchedOwner=ownerCounts.length?ownerCounts[0][0]:null;const opts=ownerCounts.map(x=>x[0]);fillSelect('ownerChoice',opts,0);$('summary').textContent=`عدد صفوف المحفظة: ${portRows.length} — لوحات لها تطابق: ${matched} — لوحات بلا تطابق: ${unmatched} — عدد الملاك المكتشفين: ${ownerCounts.length}`;$('countsTable').innerHTML=ownerCounts.length?'<table><thead><tr><th>اسم المالك في الملف الأساسي</th><th>عدد اللوحات المطابقة</th><th>الترشيح</th></tr></thead><tbody>'+ownerCounts.map(([o,c],i)=>`<tr><td>${escapeHtml(o)}</td><td>${c}</td><td>${i===0?'الأكثر تطابقًا — الاختيار الافتراضي':'متاح للاختيار'}</td></tr>`).join('')+'</tbody></table>':'<div class="status warn">لم يتم العثور على لوحات مطابقة. راجع عمود اللوحة المختار أو تأكد أن المحفظة تخص مالكًا موجودًا في الملف الأساسي.</div>';$('resultsCard').classList.remove('hidden');$('preview').classList.add('hidden');$('downloadBtn').classList.add('hidden');setStatus('portfolioStatus','اكتملت المقارنة. اختر المالك المناسب وراجع الملخص قبل التنفيذ.','good');}catch(err){setStatus('portfolioStatus','تعذّرت المقارنة: '+err.message,'warn')}});
 function escapeHtml(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
 $('previewBtn').addEventListener('click',()=>{const owner=$('ownerChoice').value;if(!owner){alert('لا يوجد مالك للاختيار.');return}const bOwner=headers[Number($('baseOwner').value)],bp=headers[Number($('basePlate').value)],pp=portHeaders[Number($('portPlate').value)];const oldCount=baseRows.filter(r=>String(r[bOwner]??'').trim()===owner).length;const newRows=portRows.filter(r=>{const pl=plateNorm(r[pp]);return pl&&baseRows.some(br=>plateNorm(br[bp])===pl&&String(br[bOwner]??'').trim()===owner)});$('preview').innerHTML=`<div class="status"><b>ملخص التحديث المقترح</b>\nالمالك المختار: ${escapeHtml(owner)}\nصفوف قديمة سيتم حذفها: ${oldCount}\nصفوف جديدة من المحفظة سيتم إضافتها: ${newRows.length}\n\nمهم: النسخة التجريبية تضيف صفوف المحفظة التي تطابقت لوحاتها مع المالك المختار. إذا كانت المحفظة تحتوي بيانات غير موجودة أصلًا في الملف الأساسي، فستحتاج مراجعة يدوية قبل اعتمادها.</div>`;$('preview').classList.remove('hidden');$('downloadBtn').classList.remove('hidden');});
 $('downloadBtn').addEventListener('click',()=>{try{const owner=$('ownerChoice').value,bOwner=headers[Number($('baseOwner').value)],bp=headers[Number($('basePlate').value)],pp=portHeaders[Number($('portPlate').value)];const oldSheet=baseWB.Sheets[chosenBaseSheet];const oldParsed=sheetData(baseWB,chosenBaseSheet);const originalAoa=oldParsed.aoa;const headerRow=oldParsed.headerRow;const newAoa=originalAoa.slice(0,headerRow+1);const keepRows=baseRows.filter(r=>String(r[bOwner]??'').trim()!==owner);const newRows=portRows.filter(r=>{const pl=plateNorm(r[pp]);return pl&&baseRows.some(br=>plateNorm(br[bp])===pl&&String(br[bOwner]??'').trim()===owner)});keepRows.forEach(r=>newAoa.push(headers.map(h=>r[h]??'')));newRows.forEach(r=>newAoa.push(headers.map(h=>{if(h===bOwner)return owner;const portKey=portHeaders.find(ph=>norm(ph)===norm(h));return portKey!==undefined?(r[portKey]??''):''})));const ws=XLSX.utils.aoa_to_sheet(newAoa);baseWB.Sheets[chosenBaseSheet]=ws;XLSX.writeFile(baseWB,'ملف_التشييك_بعد_التحديث.xlsx');setStatus('portfolioStatus','تم تنزيل نسخة محدثة. احتفظ بالملف الأصلي كنسخة احتياطية.','good');}catch(err){setStatus('portfolioStatus','تعذّر إنشاء الملف: '+err.message,'warn')}});
})();
</script>
</body>
</html>'''
path = Path("/mnt/data/mohaddeth_tashkeek.html")
path.write_text(html, encoding="utf-8")
print(f"تم إنشاء ملف الموقع: {path} — الحجم {path.stat().st_size} بايت")
