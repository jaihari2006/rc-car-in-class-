using UnrealBuildTool;
using System.Collections.Generic;

public class RCCarInClassEditorTarget : TargetRules
{
	public RCCarInClassEditorTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Editor;
		DefaultBuildSettings = BuildSettingsVersion.V5;
		IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_4;
		ExtraModuleNames.Add("RCCarInClass");
	}
}
