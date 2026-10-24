import sys, os
import win32com.client
docx = os.path.abspath(sys.argv[1])
pdf = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else None
w = win32com.client.Dispatch('Word.Application')
w.Visible = False
try:
    doc = w.Documents.Open(docx)
    doc.Repaginate()
    for t in doc.TablesOfContents:
        t.Update()
    doc.Fields.Update()
    doc.Repaginate()
    print('paginas', doc.ComputeStatistics(2))
    if sys.argv[-1] == 'guardar':
        doc.Save()
    if pdf:
        doc.ExportAsFixedFormat(pdf, 17)
    doc.Close(False)
finally:
    w.Quit()
