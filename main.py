import pymupdf
import argparse
import sys

POINT_TO_MM = 72/25.4

def main(arguments):
    doc = pymupdf.open(arguments.input_file)

    if arguments.bleed_fp is None:
        arguments.bleed_fp = arguments.bleed

    for index, page in enumerate(doc):
        bleed = arguments.bleed*POINT_TO_MM
        bleed_first_page = arguments.bleed_fp*POINT_TO_MM
        extended_box = pymupdf.Rect()
        if index == 0:
            page_size = page.mediabox
            extended_box.x0 = page_size.x0 - bleed_first_page
            extended_box.x1 = page_size.x1 + bleed_first_page
            extended_box.y0 = page_size.y0 - bleed_first_page
            extended_box.y1 = page_size.y1 + bleed_first_page
            page.set_mediabox(extended_box)
            page.set_bleedbox(page_size)

        else:
            page_size = page.mediabox
            extended_box.x0 = page_size.x0 - bleed
            extended_box.x1 = page_size.x1 + bleed
            extended_box.y0 = page_size.y0 - bleed
            extended_box.y1 = page_size.y1 + bleed
            page.set_mediabox(extended_box)
            page.set_bleedbox(page_size)

        offset = arguments.marker_offset
        marker_width = arguments.marker_width

        page.draw_line([0, bleed], [bleed-offset, bleed], width=marker_width) # left up horizontal
        page.draw_line([bleed, 0], [bleed, bleed-offset], width=marker_width) # left up vertical
        page.draw_line([extended_box.width-bleed+offset, bleed], [extended_box.width, bleed], width=marker_width) # right up horizontal
        page.draw_line([extended_box.width-bleed, 0], [extended_box.width-bleed, bleed-offset], width=marker_width) # deno up vertical
        page.draw_line([0, extended_box.height-bleed], [bleed-offset, extended_box.height-bleed], width=marker_width) # left down horizontal
        page.draw_line([bleed, extended_box.height-bleed+offset], [bleed, extended_box.height], width=marker_width) # left down vertical
        page.draw_line([extended_box.width-bleed+offset, extended_box.height-bleed], [extended_box.width, extended_box.height-bleed], width=marker_width) # right down horizontal
        page.draw_line([extended_box.width-bleed, extended_box.height-bleed+offset], [extended_box.width-bleed, extended_box.height], width=marker_width) # right down vertical

    doc_out = pymupdf.open()
    doc_out.insert_pdf(doc)
    doc_out.save(arguments.output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="PDF Print Prep",
                                     description='Program for adding bleed and print (trim) marks to the existing PDF files.')
    parser.add_argument('-b', dest='bleed', type=int, required=True, help='Bleed box size in mm. It will add the same bleed extension on all four sides.')
    parser.add_argument('-bfp', dest='bleed_fp', type= int, default=None, help='Bleed box size in mm for the first page. If parameter is not passed, [bleed] will be used.')
    parser.add_argument('-mo', dest='marker_offset', type=int, default=0, help='Marker offset in points. If offset 0, marker will touch the trim line.')
    parser.add_argument('-mw', dest='marker_width', type=float, default=0.5, help='Marker width in points. Default is 0.5.')
    parser.add_argument('-if', dest='input_file', required=True, help="Input file name.")
    parser.add_argument('-of', dest='output_file', required=True, help="Output file name.")
    
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    args = parser.parse_args()
    main(args)