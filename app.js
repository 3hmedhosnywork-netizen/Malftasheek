(() => {
  const $ = id => document.getElementById(id);
  const KEY = 'marsal-sites-v1';
  const normalize = raw => ({
    prefix: typeof raw?.prefix === 'string' ? raw.prefix : '',
    next: raw?.next === null || raw?.next === '' || raw?.next === undefined ? null : Number(raw.next),
    pendingSendId: typeof raw?.pendingSendId === 'string' ? raw.pendingSendId : null,
    items: Array.isArray(raw?.items) ? raw.items.filter(x => x && typeof x.url === 'string').map(x => ({
      id: String(x.id || (Date.now()+Math.random())), code: String(x.code || ''), url: String(x.url), sent: !!x.sent, created: Number(x.created)||Date.now()
    })) : []
  });
  let state = {prefix:'',next:null,pendingSendId:null,items:[]};
  try { state = normalize(JSON.parse(localStorage.getItem(KEY)||'{}')); } catch {}
  let installPrompt = null;
  function persist(){ localStorage.setItem(KEY,JSON.stringify(state)); render(); }
  function extractUrl(value){
    const matches=String(value||'').match(/https?:\/\/[^\s<>"']+/ig)||[];
    for(const raw of matches){ const url=raw.replace(/[),،؛.!؟]+$/,''); if(/maps\.|google\.[^/]+\/maps|goo\.gl\/maps|maps\.app\.goo\.gl/i.test(url)) return url; }
    return matches[0]?.replace(/[),،؛.!؟]+$/,'')||'';
  }
  function makeCode(){ if(!state.prefix.trim()||state.next===null||!Number.isFinite(state.next)){return '';} return state.prefix.trim()+state.next; }
  function addLink(raw, explicitCode=''){
    const url=extractUrl(raw); if(!url){notice('لم أتعرف على رابط خرائط. الصق الرابط وحاول مرة أخرى.');return false;}
    const typedCode=String(explicitCode||$('codeInput').value||'').trim();
    const code=typedCode||makeCode();
    if(!code){ $('urlInput').value=url; notice('الرابط وصل. أدخل اسم الدبوس مثل A111 أو حدد الترقيم ثم أضف الموقع.'); return false; }
    if(state.items.some(x=>x.url===url)){ $('urlInput').value=''; $('codeInput').value=''; notice('الرابط ده موجود بالفعل في القائمة.'); return false; }
    if(state.items.some(x=>x.code.toLowerCase()===code.toLowerCase())){ $('urlInput').value=url; $('codeInput').value=code; notice(`الكود ${code} موجود بالفعل. لم يتم تسجيل الموقع لتجنب التكرار.`); return false; }
    state.items.push({id:String(Date.now()+Math.random()),code,url,sent:false,created:Date.now()});
    if(!typedCode && state.next!==null && Number.isFinite(state.next)) state.next+=1;
    $('urlInput').value=''; $('codeInput').value='';notice(`تم إضافة الموقع باسم ${code}.`);persist();return true;
  }
  function extractPinCode(sharedText, title=''){
    // Inspect only the human-readable title/text before a URL; never derive a code from the URL slug.
    const sources=[String(title||''),String(sharedText||'')];
    const codePattern=/\b([A-Za-z]{1,4}[-_ ]?\d{1,5})\b/g;
    for(const source of sources){
      const beforeUrl=source.split(/https?:\/\//i)[0];
      const matches=[...beforeUrl.matchAll(codePattern)].map(m=>m[1].replace(/[-_ ]/g,''));
      if(matches.length){ return matches[matches.length-1].toUpperCase(); }
    }
    return '';
  }
  function notice(text){ $('shareNotice').textContent=text; $('shareNotice').classList.remove('hidden'); }
  // A blank line is intentionally kept between the URL and code to match the user's WhatsApp layout.
  function formatted(item){ return `${item.url}\n\n\n\n\n${item.code}`; }
  function waShare(text){ const url='https://wa.me/?text='+encodeURIComponent(text); window.open(url,'_blank'); }
  function chronological(){ return [...state.items].sort((a,b)=>a.created-b.created); }
  function render(){
    $('prefix').value=state.prefix; $('nextNumber').value=state.next??''; $('count').textContent=`${state.items.length} موقع`;
    $('queue').replaceChildren(); $('empty').classList.toggle('hidden',state.items.length>0); $('sendAllBtn').classList.toggle('hidden',state.items.length===0);
    const nextToSend=chronological().find(x=>!x.sent);
    $('sendAllBtn').textContent=state.pendingSendId?`بانتظار الرجوع من واتساب (${chronological().find(x=>x.id===state.pendingSendId)?.code||''})`:(nextToSend?`إرسال الموقع التالي (${nextToSend.code}) إلى واتساب`:'تم إرسال جميع المواقع');
    $('sendAllBtn').disabled=!nextToSend||!!state.pendingSendId;
    for(const item of chronological()){
      const card=document.createElement('article'); card.className='item';
      const top=document.createElement('div'); top.className='item-top';
      const code=document.createElement('strong'); code.className='code'; code.textContent=item.code;
      const status=document.createElement('span'); status.className='tag'+(item.sent?' done':''); status.textContent=item.sent?'تم الإرسال':(state.pendingSendId===item.id?'جارٍ الإرسال':'بانتظار الإرسال'); top.append(code,status);
      const link=document.createElement('div'); link.className='link'; link.textContent=item.url;
      const actions=document.createElement('div'); actions.className='item-actions';
      const resend=document.createElement('button'); resend.className='resend'; resend.textContent='إعادة إرسال'; resend.onclick=()=>waShare(formatted(item));
      const remove=document.createElement('button'); remove.className='delete-item'; remove.textContent='مسح الموقع'; remove.onclick=()=>{if(confirm(`حذف الموقع ${item.code} من القائمة؟`)){if(state.pendingSendId===item.id)state.pendingSendId=null;state.items=state.items.filter(x=>x.id!==item.id);persist();notice(`تم حذف الموقع ${item.code}.`);}};
      actions.append(resend,remove); card.append(top,link,actions); $('queue').append(card);
    }
  }
  $('prefix').onchange=()=>{state.prefix=$('prefix').value.trim();persist();};
  $('nextNumber').onchange=()=>{const v=$('nextNumber').value.trim();state.next=v===''?null:Math.max(0,parseInt(v,10)||0);persist();};
  $('addBtn').onclick=()=>addLink($('urlInput').value,$('codeInput').value);
  $('pasteBtn').onclick=async()=>{try{$('urlInput').value=await navigator.clipboard.readText();}catch{notice('الصق الرابط يدويًا داخل المربع.');}};
  $('clearDone').textContent='مسح الكل';
  $('clearDone').onclick=()=>{const count=state.items.length;if(!count){notice('القائمة فارغة بالفعل.');return;}if(confirm(`تأكيد مسح الكل؟ سيتم حذف جميع المواقع (${count}) بما فيها المرسلة وغير المرسلة. لا يمكن التراجع.`)){state.items=[];state.pendingSendId=null;persist();notice('تم مسح كل المواقع من القائمة.');}};
  $('sendAllBtn').onclick=()=>{const next=chronological().find(x=>!x.sent);if(!next||state.pendingSendId)return;state.pendingSendId=next.id;persist();waShare(formatted(next));notice(`تم تجهيز ${next.code}. بعد الرجوع من واتساب سيتم نقل الطابور تلقائيًا للموقع التالي.`);};
  function finishPendingSend(){if(document.visibilityState!=='visible'||!state.pendingSendId)return;const item=state.items.find(x=>x.id===state.pendingSendId);if(item&&!item.sent){item.sent=true;notice(`تم تجاوز ${item.code} وتجهيز الموقع التالي في الطابور.`);}state.pendingSendId=null;persist();}
  document.addEventListener('visibilitychange',()=>{if(!document.hidden)finishPendingSend();});
  window.addEventListener('pageshow',()=>finishPendingSend());
  function handleShared(){
    const p=new URLSearchParams(location.search);
    const title=p.get('title')||''; const text=p.get('text')||''; const urlParam=p.get('url')||'';
    const received=[urlParam,text,title].filter(Boolean).join('\n'); const url=extractUrl(received);
    const code=extractPinCode(text,title);
    if(url){
      if(code){ $('urlInput').value=url; $('codeInput').value=code; addLink(url,code); }
      else { $('urlInput').value=url; $('codeInput').value=''; notice('استلمت الرابط لكن اسم الدبوس لم يظهر في بيانات المشاركة. اكتب الاسم مثل A111 ثم اضغط إضافة الموقع؛ لن أرقّمه تلقائيًا.'); }
    }else if(received){ $('urlInput').value=received; $('codeInput').value=code; notice(code?`تم استخراج اسم الدبوس ${code}، لكن لم أجد رابط خرائط صالحًا.`:'تم استلام المشاركة، لكن لم أتمكن من استخراج اسم الدبوس والرابط.'); }
    if(received)history.replaceState({},'',location.pathname);
  }
  window.addEventListener('beforeinstallprompt',e=>{e.preventDefault();installPrompt=e;$('installBtn').classList.remove('hidden');});
  $('installBtn').onclick=async()=>{if(!installPrompt)return;installPrompt.prompt();await installPrompt.userChoice;installPrompt=null;$('installBtn').classList.add('hidden');};
  if('serviceWorker' in navigator) window.addEventListener('load',()=>navigator.serviceWorker.register('./sw.js').catch(()=>{}));
  render();handleShared();
})();
