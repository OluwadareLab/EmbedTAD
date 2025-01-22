from datetime import datetime

BASE_PATH = "/home/mohit/Documents/project/TADMaster/et_result"

with open(f"{BASE_PATH}/performance_info.txt", "w") as outfile:
    filename = f"{BASE_PATH}/embedtad_p.log"

    with open(filename, "r") as infile:
        is_start = False
        is_end = False
        is_memory = False

        start_time = None
        end_time = None
        memory = []
        lines = infile.readlines()
        info = ""
        for line in lines:
            try:
                if line.startswith("Elapsed") or line.startswith("Processing"):
                    continue
                if is_start:
                    if line.startswith("Running"):
                        outfile.write(f"{line}")
                        continue
                    elif line.startswith("Entering"):
                        # outfile.write(f"{line}")
                        continue
                    else:
                        cols = line.split(",")
                        start_time = datetime.strptime(
                            cols[0], "%Y-%m-%d %H:%M:%S")
                        is_start = False
                        is_memory = True

                if is_memory:
                    # if line.startswith("Running"):
                    #     outfile.write(f"{line}")
                    #     continue
                    # el
                    if line.startswith("Entering") or line.startswith("Elapsed") or line.startswith("Processing") or line.startswith("Running"):
                        # outfile.write(f"{line}")
                        is_end = True
                    else:
                        cols = line.split(",")
                        memory.append(int(cols[2]))
                        end_time = datetime.strptime(
                            cols[0], "%Y-%m-%d %H:%M:%S")

                if is_end:
                    peak_memory = max(memory)-min(memory)
                    elapsed_time = (end_time-start_time).total_seconds()
                    outfile.write(f"Total Time: {elapsed_time} seconds\n")
                    outfile.write(f"Peak Memory: {peak_memory} Mb\n")
                    outfile.write(f"{line}")
                    is_start = False
                    is_end = False
                    is_memory = False

                if line.startswith("Running"):
                    outfile.write(f"{line}")
                    is_start = False
                    is_end = False
                    is_memory = False
                if line.startswith("Entering"):
                    outfile.write(f"{line}")
                    is_start = True
            except Exception as ex:
                print(f"Exception at: {line}\n{ex}")
                break
        peak_memory = max(memory)-min(memory)
        elapsed_time = (end_time-start_time).total_seconds()
        outfile.write(f"Total Time: {elapsed_time} seconds\n")
        outfile.write(f"Peak Memory: {peak_memory} Mb\n")
        outfile.write(f"{line}")
