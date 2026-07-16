import sys

file_path = "drivers/misc/oplus/oplus_display_private_api.c"
with open(file_path, "rb") as f:
    content = f.read()

# Fix 1: inverted logic
target_1 = b"""\tof_ret = of_property_read_u32(pdev->dev.of_node, "oplus_display_esd_try_count", &oplus_display_esd_try_count);\r
\tif (!of_ret)\r
\t\tdev_err(&pdev->dev, "read property oplus_display_esd_try_count failed.");\r
\telse\r
\t\tDISPMSG("%s:oplus_display_esd_try_count=%u\\n", __func__, oplus_display_esd_try_count);"""

replacement_1 = b"""\tof_ret = of_property_read_u32(pdev->dev.of_node, "oplus_display_esd_try_count", &oplus_display_esd_try_count);\r
\tif (of_ret)\r
\t\tdev_err(&pdev->dev, "read property oplus_display_esd_try_count failed.\\n");\r
\telse\r
\t\tDISPMSG("%s:oplus_display_esd_try_count=%u\\n", __func__, oplus_display_esd_try_count);"""

# Fix 2: division by zero
target_2 = b"""static int interpolate(int x, int xa, int xb, int ya, int yb)\r
{\r
\tint bf, factor, plus;\r
\tint sub = 0;\r
\r
\tbf = 2 * (yb - ya) * (x - xa) / (xb - xa);\r
\tfactor = bf / 2;\r
\tplus = bf % 2;\r
\tif ((xa - xb) && (yb - ya))\r
\t\tsub = 2 * (x - xa) * (x - xb) / (yb - ya) / (xa - xb);\r
\r
\treturn ya + factor + plus + sub;\r
}"""

replacement_2 = b"""static int interpolate(int x, int xa, int xb, int ya, int yb)\r
{\r
\tint bf, factor, plus;\r
\tint sub = 0;\r
\r
\tif (xb == xa || yb == ya)\r
\t\treturn ya;\r
\r
\tbf = 2 * (yb - ya) * (x - xa) / (xb - xa);\r
\tfactor = bf / 2;\r
\tplus = bf % 2;\r
\tsub = 2 * (x - xa) * (x - xb) / (yb - ya) / (xa - xb);\r
\r
\treturn ya + factor + plus + sub;\r
}"""

# Fix 3: sscanf return checks
target_3a = b"""\tsscanf(buf, "%x", &oppo_panel_alpha);\r
\treturn count;"""
replacement_3a = b"""\tif (sscanf(buf, "%x", &oppo_panel_alpha) != 1)\r
\t\treturn -EINVAL;\r
\treturn count;"""

target_3b = b"""\tsscanf(buf, "%x", &oppo_dc_enable);\r
\treturn count;"""
replacement_3b = b"""\tif (sscanf(buf, "%x", &oppo_dc_enable) != 1)\r
\t\treturn -EINVAL;\r
\treturn count;"""

target_3c = b"""\tsscanf(buf, "%x", &oppo_dc_alpha);\r
\treturn count;"""
replacement_3c = b"""\tif (sscanf(buf, "%x", &oppo_dc_alpha) != 1)\r
\t\treturn -EINVAL;\r
\treturn count;"""

content = content.replace(target_1, replacement_1)
content = content.replace(target_2, replacement_2)
content = content.replace(target_3a, replacement_3a)
content = content.replace(target_3b, replacement_3b)
content = content.replace(target_3c, replacement_3c)

with open(file_path, "wb") as f:
    f.write(content)

print("Applied replacements via python.")
