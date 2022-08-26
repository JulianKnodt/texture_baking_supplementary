# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import math
import os
import sys
import glob
import gc
import threading
import argparse

from pathlib import Path
from simplygon10 import simplygon_loader
from simplygon10 import Simplygon


def LoadScene(sg: Simplygon.ISimplygon, path: str):
    # Create scene importer
    sgSceneImporter = sg.CreateSceneImporter()
    sgSceneImporter.SetImportFilePath(path)

    # Run scene importer.
    importResult = sgSceneImporter.Run()
    if Simplygon.Failed(importResult):
        raise Exception('Failed to load scene.')
    sgScene = sgSceneImporter.GetScene()
    return sgScene

def SaveScene(sg: Simplygon.ISimplygon, sgScene: Simplygon.spScene, path: str):
    # Create scene exporter.
    sgSceneExporter = sg.CreateSceneExporter()
    sgSceneExporter.SetExportFilePath(path)
    sgSceneExporter.SetScene(sgScene)

    # Run scene exporter.
    exportResult = sgSceneExporter.Run()
    if Simplygon.Failed(exportResult):
        raise Exception('Failed to save scene.')

def CheckLog(sg: Simplygon.ISimplygon):
    # Check if any errors occurred.
    hasErrors = sg.ErrorOccurred()
    if hasErrors:
        errors = sg.CreateStringArray()
        sg.GetErrorMessages(errors)
        errorCount = errors.GetItemCount()
        if errorCount > 0:
            print('Errors:')
            for errorIndex in range(errorCount):
                errorString = errors.GetItem(errorIndex)
                print(errorString)
            sg.ClearErrorMessages()
    else:
        print('No errors.')

    # Check if any warnings occurred.
    hasWarnings = sg.WarningOccurred()
    if hasWarnings:
        warnings = sg.CreateStringArray()
        sg.GetWarningMessages(warnings)
        warningCount = warnings.GetItemCount()
        if warningCount > 0:
            print('Warnings:')
            for warningIndex in range(warningCount):
                warningString = warnings.GetItem(warningIndex)
                print(warningString)
            sg.ClearWarningMessages()
    else:
        print('No warnings.')

def RunRemeshing(sg: Simplygon.ISimplygon, args):
    # Load scene to process.
    print(f"[INFO]: Remeshing {args.input}...")
    sgScene = LoadScene(sg, args.input)

    # Create the remeshing processor.
    sgRemeshingProcessor = sg.CreateRemeshingProcessor()
    sgRemeshingProcessor.SetScene( sgScene )
    sgRemeshingSettings = sgRemeshingProcessor.GetRemeshingSettings()

    # Set on-screen size target for remeshing.
    sgRemeshingSettings.SetOnScreenSize( args.triangle_ratio )

    sgRemeshingProcessor.RunProcessing()

    # Replace original materials and textures from the scene with a new empty material, as the
    # remeshed object has a new UV set.
    sgScene.GetTextureTable().Clear()
    sgScene.GetMaterialTable().Clear()
    sgScene.GetMaterialTable().AddMaterial( sg.CreateMaterial() )

    # Save processed scene.
    print(f"[INFO]: Saving {args.output}...")
    SaveScene(sg, sgScene, args.output)

    # Check log for any warnings or errors.
    print("Check log for any warnings or errors.")
    CheckLog(sg)

def arguments():
    a = argparse.ArgumentParser()
    a.add_argument(
        "-i", "--input", type=str, required=True,
        help="Mesh to reduce",
    )
    a.add_argument(
        "-o", "--output", type=str, required=True,
        help="Destination of reduced mesh",
    )
    a.add_argument(
        "--triangle-ratio", type=int, default=300,
        help="Compat Misnomer, screen-size to use during generation",
    )
    return a.parse_args()

if __name__ == '__main__':
        sg = simplygon_loader.init_simplygon()
        if sg is None: exit(Simplygon.GetLastInitializationError())
        RunRemeshing(sg, arguments())
        sg = None
        gc.collect()


