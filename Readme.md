### Augment Options

1) Shape Based
    scale - Up/ Down/ Random                                                | Variations 
    rotate - Min and Max angle should be selected                           | Variations    
    horizontalRotate - Left/ Right/ Both
    verticalFlip
    horizontalFlip
    Random Shear - Min and Max angle should be selected
    Resize - to a particular shape (300,300)

2) Color
    Greyscale - Yes/ No
    Brightness - Up/ Down/ Random
    Contrast - Up/ Down/ Random
    Saturation - Up/ Down/ Random
    Weird Color Changes  - **thinking**
    Blur 


3) Position and Noise
    Random Place - Select Custom Images/ Solid Colors
    Noise - Add noise on top of the region (select amount of noise allowed)
    Collage Placement - Take Multiple classes and keep it as a collage


{
    "transform" : [
                    {
                        "type" : "scale", 
                        "parameters" : {
                                            "method" : "Up"
                                        }
                        "variation" : 2
                    },

                    {
                        "type" : "Rotate", 
                        "parameters" : {
                                            "miniumAngle" : -120,
                                            "maximumAngle" : 20
                                        }
                        "variation" : 2
                    },
                    {
                        "type" : "Rotate", 
                        "parameters" : {
                                            "miniumAngle" : -180,
                                            "maximumAngle" : 20
                                        }
                        "variation" : 5
                    }
                ]
}


## image delete


##rotation

-180 - 180 : 5
90 -270 : 7
240-360 -6