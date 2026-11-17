# -*- coding: utf-8 -*-
"""Локальный обработчик корпуса для тренажёра ОГЭ, задание 11.
Работает без интернета и не отправляет файлы на сервер.
"""
import os, re, csv, zipfile, html, tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from xml.etree import ElementTree as ET

TASKS = [
 (10503, ["гнилотерк", "речк" ]),
 (10509, ["базаров"]),
 (10515, ["хома брут"]),
 (10520, ["мармеладов"]),
 (10533, ["штольц"]),
 (10536, ["владимир"]),
 (11304, ["рагин"]),
 (11308, ["ганин"]),
 (11310, ["каменного брода", "каменный брод"]),
 (11311, ["лизаньк"]),
 (11314, ["самоучка-механик", "самоучка механик", "механик"]),
 (12860, ["жалок и смешон", "казарин"]),
 (16019, ["архип елисеич"]),
 (18179, ["тревожн"]),
 (18194, ["перелетных птиц", "перелётных птиц", "крики перелетных", "крики перелётных"]),
 (18280, ["добычей радия", "добыча радия", "радия"]),
 (18295, ["тысячу аркольских мостов", "аркольских мостов"]),
 (18761, ["сладко было спознаваться"]),
 (35589, ["храм уединенного размышления", "храм уединённого размышления"]),
 (37488, ["почти весь зимний сезон", "зимний сезон"]),
 (37518, ["кот по кличке васька", "кот васька", "васька"]),
 (37687, ["взятый приучаться", "поджал хвост"]),
 (42031, ["франчески"]),
 (42058, ["младшую сестру варвары", "сестра варвары"]),
 (43660, ["екимовна"]),
]

EXTS = {'.txt','.rtf','.docx','.docm','.html','.htm','.xml','.odt'}

def norm(s):
    s = s.replace('ё','е').replace('Ё','Е').lower()
    s = re.sub(r'\s+', ' ', s)
    return s

def decode_bytes(b):
    for enc in ('utf-8-sig','utf-8','cp1251','cp866','latin-1'):
        try: return b.decode(enc)
        except UnicodeDecodeError: pass
    return b.decode('utf-8', errors='replace')

class PlainHTML(__import__('html.parser').parser.HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]
    def handle_data(self, data): self.parts.append(data)

def extract(path):
    ext=path.suffix.lower()
    if ext in ('.txt','.xml'):
        raw=decode_bytes(path.read_bytes())
        if ext=='.xml':
            try:
                root=ET.fromstring(raw)
                return '\n'.join(t for t in root.itertext() if t.strip())
            except Exception: pass
        return raw
    if ext in ('.html','.htm'):
        p=PlainHTML(); p.feed(decode_bytes(path.read_bytes())); return '\n'.join(p.parts)
    if ext=='.rtf':
        raw=decode_bytes(path.read_bytes())
        # RTF hex escapes and common control words -> readable text
        raw=re.sub(r"\\'[0-9a-fA-F]{2}", lambda m: bytes([int(m.group()[2:],16)]).decode('cp1251',errors='replace'), raw)
        raw=raw.replace('\\par','\n').replace('\\line','\n').replace('\\tab','\t')
        raw=re.sub(r'\\u(-?\d+)\??', lambda m: chr(int(m.group(1))%65536), raw)
        raw=re.sub(r'\\[a-zA-Z]+-?\d* ?', '', raw)
        raw=re.sub(r"\\[{}\\]", '', raw)
        return re.sub(r'[{}]', '', raw)
    if ext in ('.docx','.docm'):
        with zipfile.ZipFile(path) as z:
            xml=z.read('word/document.xml')
        root=ET.fromstring(xml)
        ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        paras=[]
        for p in root.findall('.//w:p',ns):
            paras.append(''.join(t.text or '' for t in p.findall('.//w:t',ns)))
        return '\n'.join(paras)
    if ext=='.odt':
        with zipfile.ZipFile(path) as z: xml=z.read('content.xml')
        root=ET.fromstring(xml)
        return '\n'.join(t for t in root.itertext() if t.strip())
    raise ValueError('Формат пока не поддерживается')

def excerpts(text, terms, radius=900):
    n=norm(text); found=[]
    for term in terms:
        t=norm(term)
        if not t: continue
        start=0
        while True:
            i=n.find(t,start)
            if i<0: break
            # Map normalized offset approximately to original offset using normalized prefix length
            # Use a normalized copy for extraction bounds, then keep original by approximate offset.
            # For whitespace/ё normalization differences, search original variants as fallback.
            found.append((i, term))
            start=i+max(1,len(t))
    if not found: return []
    # Since normalized whitespace may differ, produce excerpts from normalized text for stable offsets.
    found.sort()
    spans=[]
    for pos,term in found:
        a=max(0,pos-radius); b=min(len(n),pos+len(norm(term))+radius)
        if spans and a<=spans[-1][1]+180:
            spans[-1]=(spans[-1][0],max(spans[-1][1],b),spans[-1][2]+[term])
        else: spans.append((a,b,[term]))
    out=[]
    for a,b,ts in spans:
        chunk=n[a:b].strip()
        prefix='… ' if a else ''; suffix=' …' if b<len(n) else ''
        out.append(prefix+chunk+suffix)
    return out, len(found), sorted(set(t for _,t in found))

class App:
    def __init__(self, root):
        self.root=root; root.title('Подготовка текстов — ОГЭ, задание 11'); root.geometry('780x520')
        self.folder=tk.StringVar(); self.status=tk.StringVar(value='Выбери исходную папку с произведениями.')
        frm=ttk.Frame(root,padding=16); frm.pack(fill='both',expand=True)
        ttk.Label(frm,text='Локальная обработка корпуса текстов',font=('Segoe UI',16,'bold')).pack(anchor='w')
        ttk.Label(frm,text='Файлы остаются на твоём компьютере. Интернет и localStorage не используются.',wraplength=720).pack(anchor='w',pady=(6,16))
        line=ttk.Frame(frm); line.pack(fill='x')
        ttk.Entry(line,textvariable=self.folder).pack(side='left',fill='x',expand=True)
        ttk.Button(line,text='Выбрать папку…',command=self.pick).pack(side='left',padx=(8,0))
        ttk.Label(frm,text='Обработчик ищет фразы и ориентиры из всех 25 заданий, извлекает фрагменты с контекстом и сохраняет структуру подпапок.').pack(anchor='w',pady=16)
        self.pb=ttk.Progressbar(frm,mode='determinate'); self.pb.pack(fill='x',pady=8)
        ttk.Button(frm,text='Создать архив сокращённых текстов',command=self.run).pack(anchor='w',pady=8)
        ttk.Label(frm,textvariable=self.status,wraplength=720).pack(anchor='w',pady=8)
        self.log=tk.Text(frm,height=13,wrap='word'); self.log.pack(fill='both',expand=True,pady=(8,0))
        self.log.insert('end','Поддерживаются: TXT, RTF, DOCX, DOCM, HTML, XML, ODT. PDF и старый DOC будут перечислены как неподдерживаемые.\n')
    def pick(self):
        p=filedialog.askdirectory(title='Выбери папку с текстами')
        if p: self.folder.set(p)
    def run(self):
        base=Path(self.folder.get())
        if not base.is_dir(): messagebox.showwarning('Нет папки','Сначала выбери папку с произведениями.'); return
        files=[p for p in base.rglob('*') if p.is_file()]
        self.pb['maximum']=max(1,len(files)); self.pb['value']=0
        out=base.parent/(base.name+'_фрагменты_задание11')
        if out.exists():
            import shutil; shutil.rmtree(out)
        out.mkdir(parents=True)
        report=[]; made=0; skipped=0
        self.log.delete('1.0','end')
        for idx,p in enumerate(files,1):
            self.pb['value']=idx; self.root.update_idletasks()
            rel=p.relative_to(base); ext=p.suffix.lower()
            if ext not in EXTS:
                if ext in ('.pdf','.doc','.djvu'):
                    skipped+=1; report.append([str(rel),'Не обработан: нужен отдельный модуль', '',0])
                continue
            try: txt=extract(p)
            except Exception as e:
                skipped+=1; report.append([str(rel),'Ошибка чтения: '+str(e)[:140],'',0]); continue
            matched=[]; pieces=[]; total=0
            for tid,terms in TASKS:
                res=excerpts(txt,terms)
                if res:
                    chunks,count,used=res; matched.append(str(tid)); total+=count
                    pieces.append(f'ЗАДАНИЕ {tid}\nПоисковые ориентиры: {", ".join(used)}\n'+'\n\n'.join(chunks))
            if matched:
                dest=out/rel.parent/(p.stem+'_фрагменты.txt'); dest.parent.mkdir(parents=True,exist_ok=True)
                dest.write_text(f'Источник: {rel}\nЗадания: {", ".join(matched)}\n\n'+'\n\n'+'='*70+'\n\n'.join(pieces),encoding='utf-8-sig')
                made+=1; report.append([str(rel),'Найдены фрагменты',', '.join(matched),total])
            else:
                report.append([str(rel),'Совпадений по заданным ориентирам нет','',0])
        with (out/'Отчёт_обработки.csv').open('w',newline='',encoding='utf-8-sig') as f:
            w=csv.writer(f,delimiter=';'); w.writerow(['Исходный файл','Результат','Задания','Число совпадений']); w.writerows(report)
        zip_path=base.parent/(base.name+'_фрагменты_задание11.zip')
        with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
            for p in out.rglob('*'):
                if p.is_file(): z.write(p,p.relative_to(out))
        self.status.set(f'Готово. Файлов с фрагментами: {made}. Проблемных/неподдерживаемых: {skipped}. Архив: {zip_path}')
        self.log.insert('end',f'Создано: {zip_path}\nПапка с результатами: {out}\n\n')
        self.log.insert('end','Первые строки отчёта:\n')
        for row in report[:40]: self.log.insert('end',f'{row[0]} — {row[1]} — задания: {row[2]}\n')
        messagebox.showinfo('Готово',f'Архив создан:\n{zip_path}\n\nФайлов с фрагментами: {made}')

if __name__=='__main__':
    root=tk.Tk(); App(root); root.mainloop()
