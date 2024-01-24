import copy
import opsc
import oobb
import oobb_base
import math
import yaml

def main(**kwargs):
    make_scad(**kwargs)

def make_scad(**kwargs):
    parts = []

    # save_type variables
    if True:
        filter = ""
        #filter = []

        kwargs["save_type"] = "none"
        #kwargs["save_type"] = "all"
        
        kwargs["overwrite"] = True
        
        #kwargs["modes"] = ["3dpr", "laser", "true"]        
        kwargs["modes"] = ["3dpr"]
        #kwargs["modes"] = ["laser"]

    # default variables
    if True:
        kwargs["size"] = "oobb"
        kwargs["width"] = 12
        kwargs["height"] = 12
        thickness = 9
        kwargs["thickness"] = thickness

    # project_variables
    if True:
        #cycloidal ones
        kwargs["sockerbit_lip_width"] = 15
        kwargs["sockerbit_lip_depth"] = 15
        kwargs["sokerbit_plastic_thickness"] = 2
        kwargs["bin_spacing"] = 5
        kwargs["thickness_default"] = 3
        

    
    # declare parts
    if True:
        part_default = {} 
        part_default["project_name"] = "oomlout_storage_ikea_sockerbit_stadium_seating_configuration"
        part_default["full_shift"] = [0, 0, 0]
        part_default["full_rotations"] = [0, 0, 0]
        
        part = copy.deepcopy(part_default)
        p3 = copy.deepcopy(kwargs)
        p3["thickness"] = thickness
        part["kwargs"] = p3
        part["name"] = "clamp_top"        
        parts.append(part)
        
        part = copy.deepcopy(part_default)
        p3 = copy.deepcopy(kwargs)
        p3["thickness"] = thickness
        part["kwargs"] = p3
        part["name"] = "clamp_bottom"        
        parts.append(part)

        
    #make the parts
    if True:
        for part in parts:
            name = part.get("name", "default")            
            if not isinstance(filter, list):
                filter = [filter]
            generate = False
            for f in filter:
                if f in name:
                    generate = True
            if generate:
                print(f"making {part['name']}")
                make_scad_generic(part)            
                print(f"done {part['name']}")
            else:
                print(f"skipping {part['name']}")

    #dump parts to scad_output/working.yaml
    if True:
        yaml_file = "scad_output/working.yaml"
        with open(yaml_file, 'w') as file:
            part_details = {}
            counter = 1
            for part in parts:
                name = part["kwargs"].get("type", "default")
                part_details[name] = part
                counter += 1
            yaml.dump(part_details, file)
    


def get_clamp_bottom(thing, **kwargs):
    center_offset = kwargs.get("center_offset", True)

    thickness = kwargs.get("thickness", 4)
    prepare_print = kwargs.get("prepare_print", True)

    pos = kwargs.get("pos", [0, 0, 0])
    #pos = copy.deepcopy(pos)
    #pos[2] += -20


    #varaiables
    sokerbit_lip_width  = kwargs.get("sockerbit_lip_width", 15)
    sokerbit_lip_depth  = kwargs.get("sockerbit_lip_depth", 15)
    sokerbit_plastic_thickness  = kwargs.get("sokerbit_plastic_thickness", 2)
    bin_spacing  = kwargs.get("bin_spacing", 5)
    thickness_default  = kwargs.get("thickness_default", 3)


    #add _cube_middle
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_cube"
    width = bin_spacing
    height = sokerbit_lip_depth
    depth = thickness
    p3["size"] = [width, height, depth]   
    pos1 = copy.deepcopy(pos)     
    pos1[1] += -sokerbit_lip_depth/2
    pos1[2] += -depth/2
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    #add cube_cross
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_cube"
    width = bin_spacing + 2 * sokerbit_lip_width
    height = thickness_default
    depth = thickness
    p3["size"] = [width, height, depth]   
    pos1 = copy.deepcopy(pos)     
    pos1[1] += -sokerbit_lip_depth - thickness_default/2
    pos1[2] += -depth/2
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    # add joining screw
    get_joining_screw(thing, **kwargs)


    if prepare_print:
        #put into a rotation object
        if False:
            components_second = copy.deepcopy(thing["components"])
            return_value_2 = {}
            return_value_2["type"]  = "rotation"
            return_value_2["typetype"]  = "p"
            pos1 = copy.deepcopy(pos)
            pos1[0] += 50
            return_value_2["pos"] = pos1
            return_value_2["rot"] = [180,0,0]
            return_value_2["objects"] = components_second
            
            thing["components"].append(return_value_2)

        
            #add slice # top
            p3 = copy.deepcopy(kwargs)
            p3["type"] = "n"
            p3["shape"] = f"oobb_slice"
            #p3["m"] = "#"
            oobb_base.append_full(thing,**p3)
    

def get_clamp_top(thing, **kwargs):
    center_offset = kwargs.get("center_offset", True)

    thickness = kwargs.get("thickness", 4)
    prepare_print = kwargs.get("prepare_print", True)

    pos = kwargs.get("pos", [0, 0, 0])
    #pos = copy.deepcopy(pos)
    #pos[2] += -20


    #varaiables
    sokerbit_lip_width  = kwargs.get("sockerbit_lip_width", 15)
    sokerbit_lip_depth  = kwargs.get("sockerbit_lip_depth", 15)
    sokerbit_plastic_thickness  = kwargs.get("sokerbit_plastic_thickness", 2)
    bin_spacing  = kwargs.get("bin_spacing", 5)
    thickness_default  = kwargs.get("thickness_default", 3)


    #add _cube_middle
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_cube"
    width = bin_spacing + 2 * sokerbit_lip_width + thickness_default * 2
    height = thickness_default
    depth = thickness
    p3["size"] = [width, height, depth]   
    pos1 = copy.deepcopy(pos)     
    pos1[1] += thickness_default/2
    pos1[2] += -depth/2
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    #add down x 2
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_cube"
    width = thickness_default
    height = sokerbit_lip_depth
    depth = thickness
    p3["size"] = [width, height, depth]   
    poss = []
    pos1 = copy.deepcopy(pos)     
    pos1[2] += -depth/2
    pos11 = copy.deepcopy(pos1)
    pos11[0] += -bin_spacing / 2 - sokerbit_lip_width - thickness_default / 2
    pos11[1] += -sokerbit_lip_depth / 2
    pos12 = copy.deepcopy(pos1)
    pos12[0] += bin_spacing / 2 + sokerbit_lip_width + thickness_default / 2
    pos12[1] += -sokerbit_lip_depth / 2
    poss.append(pos11)
    poss.append(pos12)
    p3["pos"] = poss
    oobb_base.append_full(thing,**p3)

    # add joining screw
    get_joining_screw(thing, **kwargs)


    if prepare_print:
        #put into a rotation object
        if False:
            components_second = copy.deepcopy(thing["components"])
            return_value_2 = {}
            return_value_2["type"]  = "rotation"
            return_value_2["typetype"]  = "p"
            pos1 = copy.deepcopy(pos)
            pos1[0] += 50
            return_value_2["pos"] = pos1
            return_value_2["rot"] = [180,0,0]
            return_value_2["objects"] = components_second
            
            thing["components"].append(return_value_2)

        
            #add slice # top
            p3 = copy.deepcopy(kwargs)
            p3["type"] = "n"
            p3["shape"] = f"oobb_slice"
            #p3["m"] = "#"
            oobb_base.append_full(thing,**p3)
    





def get_joining_screw(thing, **kwargs):
    #varaiables
    pos = kwargs.get("pos", [0, 0, 0])
    sokerbit_lip_width  = kwargs.get("sockerbit_lip_width", 15)
    sokerbit_lip_depth  = kwargs.get("sockerbit_lip_depth", 15)
    sokerbit_plastic_thickness  = kwargs.get("sokerbit_plastic_thickness", 2)
    bin_spacing  = kwargs.get("bin_spacing", 5)
    thickness_default  = kwargs.get("thickness_default", 3)
    #add joining_screw
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_screw_countersunk"
    p3["radius_name"] = "m3"
    p3["depth"] = thickness_default * 2 + sokerbit_lip_depth
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)     
    pos1[1] += thickness_default
    p3["pos"] = pos1
    p3["nut"] = True
    p3["rot"] = [-90,0,0]
    #p3["m"] = "#"
    oobb_base.append_full(thing,**p3)











###### utilities



def make_scad_generic(part):
    
    # fetching variables
    name = part.get("name", "default")
    project_name = part.get("project_name", "default")
    
    kwargs = part.get("kwargs", {})    
    
    modes = kwargs.get("modes", ["3dpr", "laser", "true"])
    save_type = kwargs.get("save_type", "all")
    overwrite = kwargs.get("overwrite", True)

    kwargs["type"] = f"{project_name}_{name}"

    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size","")

    #get the part from the function get_{name}"
    func = globals()[f"get_{name}"]
    func(thing, **kwargs)

    for mode in modes:
        depth = thing.get(
            "depth_mm", thing.get("thickness_mm", 3))
        height = thing.get("height_mm", 100)
        layers = depth / 3
        tilediff = height + 10
        start = 1.5
        if layers != 1:
            start = 1.5 - (layers / 2)*3
        if "bunting" in thing:
            start = 0.5
        opsc.opsc_make_object(f'scad_output/{thing["id"]}/{mode}.scad', thing["components"], mode=mode, save_type=save_type, overwrite=overwrite, layers=layers, tilediff=tilediff, start=start)    


if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)