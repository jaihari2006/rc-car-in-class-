#pragma once

#include "CoreMinimal.h"
#include "WheeledVehiclePawn.h"
#include "RCCarPawn.generated.h"

class USpringArmComponent;
class UCameraComponent;
class UAudioComponent;
class UNiagaraComponent;
class UPointLightComponent;
class USpotLightComponent;

UCLASS()
class RCCARINCLASS_API ARCCarPawn : public AWheeledVehiclePawn
{
	GENERATED_BODY()

public:
	ARCCarPawn();

	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;
	virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

	// Input Handlers
	void ApplyThrottle(float AxisValue);
	void ApplySteering(float AxisValue);
	void ApplyHandbrake(bool bBraking);
	void StartNitro();
	void StopNitro();
	void ResetCar();
	void ToggleCameraMode();

	// Car Attributes
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RC Car | Stats")
	FString CarName = TEXT("Blue Horizon Porsche 911 GTS");

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RC Car | Nitro")
	float MaxNitro = 100.0f;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "RC Car | Nitro")
	float CurrentNitro = 100.0f;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "RC Car | Nitro")
	bool bIsNitroActive = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RC Car | Nitro")
	float NitroDrainRate = 35.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RC Car | Nitro")
	float NitroRefillRate = 12.0f;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "RC Car | Physics")
	float CurrentSpeedKmh = 0.0f;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "RC Car | Physics")
	float NormalizedRPM = 0.0f;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "RC Car | Physics")
	float DriftSlipRatio = 0.0f;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "RC Car | Status")
	bool bIsCaughtBySensei = false;

protected:
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera")
	USpringArmComponent* SpringArm;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera")
	UCameraComponent* ChaseCamera;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera")
	UCameraComponent* TopDownCamera;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Lights")
	USpotLightComponent* HeadlightLeft;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Lights")
	USpotLightComponent* HeadlightRight;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Lights")
	UPointLightComponent* UnderglowLight;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Audio")
	UAudioComponent* EngineAudioComponent;

private:
	bool bUseTopDownCamera = false;
	FVector SpawnLocation;
	FRotator SpawnRotation;
};
