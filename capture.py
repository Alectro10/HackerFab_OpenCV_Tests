
import PySpin

system = PySpin.System.GetInstance()
cameras = system.GetCameras()

if cameras.GetSize() == 0:
    print("No camera found")
else:
    camera = cameras.GetByIndex(0)
    camera.Init()

    try:
        camera.AcquisitionMode.SetValue(
            PySpin.AcquisitionMode_Continuous
        )
        camera.BeginAcquisition()

        try:
            image = camera.GetNextImage(5000)

            try:
                if not image.IsIncomplete():
                    converted = image.Convert(
                        PySpin.PixelFormat_Mono8,
                        PySpin.HQ_LINEAR
                    )
                    converted.Save("wafer.jpg")
                    print("Picture saved!")
                else:
                    print("Image was incomplete")
            finally:
                image.Release()
        finally:
            camera.EndAcquisition()
    finally:
        camera.DeInit()
        del camera

cameras.Clear()
system.ReleaseInstance()
