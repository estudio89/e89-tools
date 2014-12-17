# -*- coding: utf-8 -*-
import csv
import cStringIO
import codecs

class UnicodeWriter:
    ''' Utilizado junto com a biblioteca geraldo_reports para escrever arquivos CSV que contêm caracteres unicode.

        Ex:
            relatorio = accounts.reports.AlertasReport(request.user.usercrmv,ramos=ramos,delegacias=delegacias,data_filtro=data_filtro)
            resp = HttpResponse(content_type='text/csv')

            from geraldo.generators import CSVGenerator
            import tools.report_tools
            relatorio.generate_by(CSVGenerator, filename=resp,writer=tools.report_tools.UnicodeWriter(resp))

        '''
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
    def writerow(self, row):
        '''writerow(unicode) -> None
        This function takes a Unicode string and encodes it to the output.
        '''
        self.writer.writerow([s.encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def drop_shadow( image, offset=(5,5), background=0xffffff, shadow=0x444444,
                border=8, iterations=3):
    """
    Add a gaussian blur drop shadow to an image.

    image       - The image to overlay on top of the shadow.
    offset      - Offset of the shadow from the image as an (x,y) tuple.  Can be
                positive or negative.
    background  - Background colour behind the image.
    shadow      - Shadow colour (darkness).
    border      - Width of the border around the image.  This must be wide
                enough to account for the blurring of the shadow.
    iterations  - Number of times to apply the filter.  More iterations
                produce a more blurred shadow, but increase processing time.
    """

    # Create the backdrop image -- a box in the background colour with a
    # shadow on it.
    totalWidth = image.size[0] + abs(offset[0]) + 2*border
    totalHeight = image.size[1] + abs(offset[1]) + 2*border
    back = Image.new(image.mode, (totalWidth, totalHeight), background)

    # Place the shadow, taking into account the offset from the image
    shadowLeft = border + max(offset[0], 0)
    shadowTop = border + max(offset[1], 0)
    back.paste(shadow, [shadowLeft, shadowTop, shadowLeft + image.size[0],
        shadowTop + image.size[1]] )

    # Apply the filter to blur the edges of the shadow.  Since a small kernel
    # is used, the filter must be applied repeatedly to get a decent blur.
    n = 0
    while n < iterations:
        back = back.filter(ImageFilter.BLUR)
        n += 1

    # Paste the input image onto the shadow backdrop
    imageLeft = border - min(offset[0], 0)
    imageTop = border - min(offset[1], 0)
    back.paste(image, (imageLeft, imageTop))

    return back