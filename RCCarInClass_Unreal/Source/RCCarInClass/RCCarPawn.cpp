#include "RCCarPawn.h"
#include "GameFramework/SpringArmComponent.h"
#include "Camera/CameraComponent.h"
#include "Components/AudioComponent.h"
#include "Components/SpotLightComponent.h"
#include "Components/PointLightComponent.h"
#include "ChaosWheeledVehicleMovementComponent.h"
#include "RCCarInClass.h"

ARCCarPawn::ARCCarPawn()
{
	PrimaryActorTick.bCanEverTick = true;

	// Spring Arm for Chase Camera
	SpringArm = CreateDefaultSubobject<USpringArmComponent>(TEXT("SpringArm"));
	SpringArm->SetupAttachment(RootComponent);
	SpringArm->TargetArmLength = 450.0f;
	SpringArm->SocketOffset = FVector(0.0f, 0.0f, 120.0f);
	SpringArm->bEnableCameraLag = true;
	SpringArm->CameraLagSpeed = 12.0f;
	SpringArm->bEnableCameraRotationLag = true;
	SpringArm->CameraRotationLagSpeed = 10.0f;
	SpringArm->bInheritPitch = false;
	SpringArm->bInheritRoll = false;

	// Chase Camera
	ChaseCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("ChaseCamera"));
	ChaseCamera->SetupAttachment(SpringArm, USpringArmComponent::SocketName);
	ChaseCamera->SetRelativeRotation(FRotator(-15.0f, 0.0f, 0.0f));

	// Picture-in-Picture Bird's Eye View Camera
	TopDownCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("TopDownCamera"));
	TopDownCamera->SetupAttachment(RootComponent);
	TopDownCamera->SetRelativeLocation(FVector(0.0f, 0.0f, 950.0f));
	TopDownCamera->SetRelativeRotation(FRotator(-90.0f, 0.0f, 0.0f));
	TopDownCamera->bAutoActivate = false;

	// Front Headlights
	HeadlightLeft = CreateDefaultSubobject<USpotLightComponent>(TEXT("HeadlightLeft"));
	HeadlightLeft->SetupAttachment(RootComponent);
	HeadlightLeft->SetRelativeLocation(FVector(80.0f, -25.0f, 20.0f));
	HeadlightLeft->SetLightColor(FLinearColor(1.0f, 0.95f, 0.85f));
	HeadlightLeft->Intensity = 3000.0f;

	HeadlightRight = CreateDefaultSubobject<USpotLightComponent>(TEXT("HeadlightRight"));
	HeadlightRight->SetupAttachment(RootComponent);
	HeadlightRight->SetRelativeLocation(FVector(80.0f, 25.0f, 20.0f));
	HeadlightRight->SetLightColor(FLinearColor(1.0f, 0.95f, 0.85f));
	HeadlightRight->Intensity = 3000.0f;

	// Neon Cyan Underglow
	UnderglowLight = CreateDefaultSubobject<UPointLightComponent>(TEXT("UnderglowLight"));
	UnderglowLight->SetupAttachment(RootComponent);
	UnderglowLight->SetRelativeLocation(FVector(0.0f, 0.0f, 5.0f));
	UnderglowLight->SetLightColor(FLinearColor(0.0f, 0.9f, 1.0f));
	UnderglowLight->Intensity = 800.0f;
	UnderglowLight->AttenuationRadius = 120.0f;

	// Engine Audio Component
	EngineAudioComponent = CreateDefaultSubobject<UAudioComponent>(TEXT("EngineAudioComponent"));
	EngineAudioComponent->SetupAttachment(RootComponent);
	EngineAudioComponent->bAutoActivate = true;
}

void ARCCarPawn::BeginPlay()
{
	super::BeginPlay();
	SpawnLocation = GetActorLocation();
	SpawnRotation = GetActorRotation();
	CurrentNitro = MaxNitro;
}

void ARCCarPawn::Tick(float DeltaTime)
{
	super::Tick(DeltaTime);

	UChaosWheeledVehicleMovementComponent* Movement = Cast<UChaosWheeledVehicleMovementComponent>(GetVehicleMovementComponent());
	if (Movement)
	{
		CurrentSpeedKmh = FMath::Abs(Movement->GetForwardSpeed()) * 0.036f;
		NormalizedRPM = FMath::Clamp(Movement->GetEngineRotationSpeed() / 7500.0f, 0.15f, 1.0f);

		// Calculate drift slip angle
		FVector VelocityNorm = GetVelocity().GetSafeNormal2D();
		FVector ForwardNorm = GetActorForwardVector().GetSafeNormal2D();
		DriftSlipRatio = 1.0f - FMath::Abs(FVector::DotProduct(VelocityNorm, ForwardNorm));

		// Update audio parameters for flat-6 engine pitch & volume
		if (EngineAudioComponent)
		{
			EngineAudioComponent->SetFloatParameter(FName("RPM"), NormalizedRPM);
			EngineAudioComponent->SetFloatParameter(FName("Speed"), CurrentSpeedKmh);
			EngineAudioComponent->SetBoolParameter(FName("NitroOn"), bIsNitroActive);
		}
	}

	// Handle Nitro usage & passive refill
	if (bIsNitroActive)
	{
		CurrentNitro = FMath::Max(0.0f, CurrentNitro - NitroDrainRate * DeltaTime);
		if (CurrentNitro <= 0.0f)
		{
			StopNitro();
		}
	}
	else
	{
		CurrentNitro = FMath::Min(MaxNitro, CurrentNitro + NitroRefillRate * DeltaTime);
	}
}

void ARCCarPawn::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	super::SetupPlayerInputComponent(PlayerInputComponent);

	PlayerInputComponent->BindAxis("Throttle", this, &ARCCarPawn::ApplyThrottle);
	PlayerInputComponent->BindAxis("Steering", this, &ARCCarPawn::ApplySteering);

	PlayerInputComponent->BindAction("Nitro", IE_Pressed, this, &ARCCarPawn::StartNitro);
	PlayerInputComponent->BindAction("Nitro", IE_Released, this, &ARCCarPawn::StopNitro);

	PlayerInputComponent->BindAction("ResetCar", IE_Pressed, this, &ARCCarPawn::ResetCar);
	PlayerInputComponent->BindAction("ToggleCamera", IE_Pressed, this, &ARCCarPawn::ToggleCameraMode);
}

void ARCCarPawn::ApplyThrottle(float AxisValue)
{
	if (bIsCaughtBySensei) return;

	UChaosWheeledVehicleMovementComponent* Movement = Cast<UChaosWheeledVehicleMovementComponent>(GetVehicleMovementComponent());
	if (Movement)
	{
		float BoostMultiplier = bIsNitroActive ? 1.65f : 1.0f;
		Movement->SetThrottleInput(FMath::Clamp(AxisValue * BoostMultiplier, -1.0f, 1.0f));
	}
}

void ARCCarPawn::ApplySteering(float AxisValue)
{
	if (bIsCaughtBySensei) return;

	UChaosWheeledVehicleMovementComponent* Movement = Cast<UChaosWheeledVehicleMovementComponent>(GetVehicleMovementComponent());
	if (Movement)
	{
		Movement->SetSteeringInput(AxisValue);
	}
}

void ARCCarPawn::ApplyHandbrake(bool bBraking)
{
	UChaosWheeledVehicleMovementComponent* Movement = Cast<UChaosWheeledVehicleMovementComponent>(GetVehicleMovementComponent());
	if (Movement)
	{
		Movement->SetHandbrakeInput(bBraking);
	}
}

void ARCCarPawn::StartNitro()
{
	if (CurrentNitro > 10.0f && !bIsCaughtBySensei)
	{
		bIsNitroActive = true;
	}
}

void ARCCarPawn::StopNitro()
{
	bIsNitroActive = false;
}

void ARCCarPawn::ResetCar()
{
	SetActorLocation(SpawnLocation + FVector(0.0f, 0.0f, 20.0f));
	SetActorRotation(SpawnRotation);

	UChaosWheeledVehicleMovementComponent* Movement = Cast<UChaosWheeledVehicleMovementComponent>(GetVehicleMovementComponent());
	if (Movement)
	{
		Movement->StopMovementImmediately();
	}
	bIsCaughtBySensei = false;
	bIsNitroActive = false;
}

void ARCCarPawn::ToggleCameraMode()
{
	bUseTopDownCamera = !bUseTopDownCamera;
	ChaseCamera->SetActive(!bUseTopDownCamera);
	TopDownCamera->SetActive(bUseTopDownCamera);
}
