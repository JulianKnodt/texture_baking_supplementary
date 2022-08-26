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

def RunReduction(sg: Simplygon.ISimplygon, args):
    # Load scene to process.
    print("Load scene to process.")
    sgScene = LoadScene(sg, args.input)

    # Create the reduction processor.
    sgReductionProcessor = sg.CreateReductionProcessor()
    sgReductionProcessor.SetScene( sgScene )
    sgReductionSettings = sgReductionProcessor.GetReductionSettings()

    # Set reduction target to triangle ratio with a ratio of 50%.
    sgReductionSettings.SetReductionTargets( Simplygon.EStopCondition_All, True, False, False, False )
    sgReductionSettings.SetReductionTargetTriangleRatio(args.triangle_ratio)
    sgReductionSettings.SetAllowDegenerateTexCoords(False)
    sgReductionSettings.SetMergeGeometries(True)


    sgRepairSettings = sgReductionProcessor.GetRepairSettings()
    sgRepairSettings.SetProgressivePasses(3)
    sgRepairSettings.SetUseWelding( True )
    sgRepairSettings.SetWeldDist( 0.0 )

    # Remove T-junctions. 
    sgRepairSettings.SetUseTJunctionRemover( True )
    sgRepairSettings.SetTJuncDist( 0.0 )

    # No restriction to the weld process. 
    sgRepairSettings.SetWeldOnlyBetweenSceneNodes( False )
    sgRepairSettings.SetWeldOnlyBorderVertices( False )
    sgRepairSettings.SetWeldOnlyWithinMaterial( False )
    sgRepairSettings.SetWeldOnlyWithinSceneNode( False )

    # Start the reduction process.
    print(f"[INFO]: Starting reduction of {args.input} at {args.triangle_ratio}...")
    sgReductionProcessor.RunProcessing()

    # Save processed scene.
    print(f"[INFO]: Saving reduced scene to {args.output}...")
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
        "--triangle-ratio", type=float, default=0.5,
        help="Value in (0,1) for ratio of faces to retain",
    )
    return a.parse_args()

if __name__ == '__main__':
        sg = simplygon_loader.init_simplygon()
        if sg is None: exit(Simplygon.GetLastInitializationError())

        RunReduction(sg, arguments())

        sg = None
        gc.collect()

