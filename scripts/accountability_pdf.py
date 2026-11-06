"""Render the one-page accountability sheet; optional ReportLab dependency for docs only."""
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('RelayfySans','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('RelayfySansBold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
root=Path(__file__).resolve().parents[1]
text=(root/'submission/02_accountability_sheet.md').read_text()
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleR',fontName='RelayfySansBold',fontSize=24,leading=29,textColor=HexColor('#202224'),spaceAfter=8))
styles.add(ParagraphStyle(name='SubR',fontName='RelayfySans',fontSize=9,leading=13,textColor=HexColor('#686b6d'),spaceAfter=14))
styles.add(ParagraphStyle(name='BodyR',fontName='RelayfySans',fontSize=8.4,leading=12,textColor=HexColor('#373b3e')))
styles.add(ParagraphStyle(name='KeyR',fontName='RelayfySansBold',fontSize=8.3,leading=12,textColor=HexColor('#bd4c27')))
styles.add(ParagraphStyle(name='FootR',fontName='RelayfySans',fontSize=8.1,leading=12,textColor=HexColor('#74797c')))
rows=[]
for line in text.splitlines():
    if line.startswith('|') and not line.startswith('|---') and not line.startswith('| Area'):
        cells=[c.strip().replace('“','"').replace('”','"').replace('→','to').replace('–','-').replace('—','-') for c in line.strip('|').split('|')]
        rows.append([Paragraph(escape(cells[0]),styles['KeyR']),Paragraph(escape(cells[1]),styles['BodyR'])])
doc=SimpleDocTemplate(str(root/'submission/02_accountability_sheet.pdf'),pagesize=(595.28,841.89),leftMargin=38,rightMargin=38,topMargin=36,bottomMargin=35)
table=Table(rows,colWidths=[104,415.28],hAlign='LEFT')
table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('ROWBACKGROUNDS',(0,0),(-1,-1),[HexColor('#f3f4f4'),HexColor('#fafafa')]),('LINEBELOW',(0,0),(-1,-1),.5,HexColor('#e1e3e4'))]))
footer='Sebelum data nyata: verifikasi identitas, model, isolasi agent, HTTPS, volume/backup dan evaluasi independen. Demo dan klik otomatis pada pengujian bukan persetujuan pengguna bisnis nyata.'
story=[Paragraph('RELAYFY',styles['SubR']),Paragraph('Accountability sheet',styles['TitleR']),Paragraph('Salman Fidinillah | Challenge A | Web + WorkBuddy runtime | Data sintetis | 4 November 2026',styles['SubR']),table,Spacer(1,15),Paragraph(footer,styles['FootR'])]
def page(canvas,doc):
    canvas.setTitle('Relayfy - Accountability Sheet')
    canvas.setAuthor('Salman Fidinillah')
    canvas.setStrokeColor(HexColor('#e1e3e4'));canvas.line(38,30,557,30)
    canvas.setFont('Helvetica',7);canvas.setFillColor(HexColor('#74797c'));canvas.drawString(38,19,'Relayfy - prepared locally; local tests verified; actual WorkBuddy/model evidence pending.');canvas.drawRightString(557,19,str(doc.page))
doc.build(story,onFirstPage=page,onLaterPages=page)
print('Accountability PDF rendered')
