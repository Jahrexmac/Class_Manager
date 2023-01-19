from reportlab.platypus import Table,SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import io

def generate_result_pdf(class_result):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=12, rightMargin=12, bottomMargin=18, topMargin=20)
    story = []
    styles = getSampleStyleSheet()
    ptext= f"<para align='center'><font size=16>{class_result[0]['student_class']} RESULT</font></para>"
    story.append(Paragraph(ptext, styles['Normal']))
    story.append(Spacer(1,12))
    tblstyle = [
            ('BACKGROUND', (0,0), (-1,1), colors.green),
            ('TEXTCOLOR', (0,0), (-1,1), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTSIZE', (0,0), (-1,1), 14),
            ('FONTSIZE', (0,1), (-1,-1), 10),     
        ]
   
    for result in class_result:
        ptext= f"<para leftIndent=20 leading=15 ><font size=14>{result['name']}</font></para>"
        story.append(Paragraph(ptext, styles['Normal']))
        story.append(Spacer(1,12))
        data = [
            [f"GrandTotal: {result['grand_total']}",'', '','',f"Position: {result['position']}",'','',f"Average (%): {result['average']}"],
            ['S/n', 'Subject', 'First Test', 'Second Test', 'Exam', 'Total', 'Grade', 'Remark'],
        ]
        row = 2 # keep track of subject rows
        for subject in result['subject']:
            if int(subject.total) < 40:
               tblstyle.append(('TEXTCOLOR', (0,row), (-1,row), colors.red))
               data.append([subject.serial_number, subject.name, subject.first_test, subject.second_test, subject.exam, subject.total, subject.grade, subject.remark]) 
            else:
                tblstyle.append(('TEXTCOLOR', (0,row), (-1,row), colors.black))
                data.append([subject.serial_number, subject.name, subject.first_test, subject.second_test, subject.exam, subject.total, subject.grade, subject.remark]) 

            row += 1 
        tbl= Table(data)
        tbl.setStyle(tblstyle)
        story.append(tbl)
        story.append(Spacer(0,40))

    doc.build(story)
    buffer.seek(0)
    return buffer
    


    
