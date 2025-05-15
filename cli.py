import typer
import numpy
from typing_extensions import Annotated
from libifcb import ROIReader
from ifcb_feature_extractor.all import compute_features
import time
import csv
import math

def main(
    hdr_file: Annotated[str, typer.Argument(help="The HDR file from your IFCB sample")],
    adc_file: Annotated[str, typer.Option("--adc", help="The ADC file from your IFCB sample (this can usually be auto-detected and can be omitted)")] = None,
    roi_file: Annotated[str, typer.Option("--roi", help="The ROI file from your IFCB sample (this can usually be auto-detected and can be omitted)")] = None,
    csv_file: Annotated[str, typer.Option("-o", "--out", help="The output CSV file for feature information")] = None
):
    if adc_file is None:
        adc_file = hdr_file[:-4] + ".adc"
    if roi_file is None:
        roi_file = hdr_file[:-4] + ".roi"
    if csv_file is None:
        csv_file = hdr_file[:-4] + "_features.csv"

    sample = ROIReader(hdr_file, adc_file, roi_file)
    #print(sample.rois)

    first = True
    orig_time = time.time()
    with open(csv_file, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=",", quotechar="\"", quoting=csv.QUOTE_MINIMAL)
        adc_row_idx = 0
        total_rows = len(sample.rows)
        for adc_row_image in sample.rows:
            adc_row_idx += 1
            #adc_data_row = sample.adc_data[adc_row_idx-1]
            if adc_row_image is not None:
                row_features_tup = compute_features(numpy.asarray(adc_row_image), None, None)[1]
                row_features = {}
                for feat in row_features_tup:
                    row_features[feat[0]] = feat[1]
                if first:
                    first = False
                    csv_writer.writerow(["roi_number", *row_features.keys()])
                csv_writer.writerow([adc_row_idx, *row_features.values()])

            if adc_row_idx % 16 == 0:
                bar_w = 32
                bar_x = round(bar_w * (adc_row_idx/total_rows))
                bar_l = "#"*bar_x
                bar_r = "_"*(bar_w - bar_x)
                ttime = ((time.time() - orig_time) / adc_row_idx) * total_rows
                if adc_row_idx > 5:
                    secs = round(ttime * (1 - (adc_row_idx/total_rows)))
                    timestr = f"about {secs}s remaining..."
                    if secs < 3:
                        timestr = "only a few seconds remaining..."
                    if secs > 60:
                        mins = math.floor(secs / 60)
                        secs = secs - (mins * 60)
                        timestr = f"about {mins}min {secs}s remaining..."
                    if secs > 3600:
                        hrs = math.floor(mins / 60)
                        mins = mins - (hrs * 60)
                        timestr = f"about {hrs}hr {mins}min remaining..."

                    print(f"\r[{bar_l}{bar_r}] {timestr}                ", end="")
                else:
                    print(f"\r[{bar_l}{bar_r}] getting ready...", end="")
        #print(adc_data_row)
        #print(row_features)


if __name__ == "__main__":
    typer.run(main)
