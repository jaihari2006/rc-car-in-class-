#include "HomeworkPaperPickup.h"
#include "Components/SphereComponent.h"
#include "Components/StaticMeshComponent.h"
#include "GameFramework/RotatingMovementComponent.h"
#include "Kismet/GameplayStatics.h"
#include "RCCarPawn.h"
#include "ClassroomGameMode.h"

AHomeworkPaperPickup::AHomeworkPaperPickup()
{
	PrimaryActorTick.bCanEverTick = true;

	CollisionSphere = CreateDefaultSubobject<USphereComponent>(TEXT("CollisionSphere"));
	RootComponent = CollisionSphere;
	CollisionSphere->SetSphereRadius(60.0f);
	CollisionSphere->SetCollisionProfileName(TEXT("OverlapAllDynamic"));

	PaperMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("PaperMesh"));
	PaperMesh->SetupAttachment(RootComponent);
	PaperMesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);

	RotatingMovement = CreateDefaultSubobject<URotatingMovementComponent>(TEXT("RotatingMovement"));
	RotatingMovement->RotationRate = FRotator(0.0f, 90.0f, 0.0f);
}

void AHomeworkPaperPickup::BeginPlay()
{
	super::BeginPlay();
	CollisionSphere->OnComponentBeginOverlap.AddDynamic(this, &AHomeworkPaperPickup::OnOverlapBegin);
}

void AHomeworkPaperPickup::Tick(float DeltaTime)
{
	super::Tick(DeltaTime);
	// Gentle bobbing motion
	float BobOffset = FMath::Sin(GetWorld()->GetTimeSeconds() * 3.0f) * 0.4f;
	AddActorWorldOffset(FVector(0.0f, 0.0f, BobOffset));
}

void AHomeworkPaperPickup::OnOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor,
                                         UPrimitiveComponent* OtherComp, int32 OtherBodyIndex,
                                         bool bFromSweep, const FHitResult& SweepResult)
{
	ARCCarPawn* Car = Cast<ARCCarPawn>(OtherActor);
	if (Car)
	{
		AClassroomGameMode* GM = Cast<AClassroomGameMode>(UGameplayStatics::GetGameMode(GetWorld()));
		if (GM)
		{
			GM->AddScore(PointValue, CoinValue);
		}

		Destroy();
	}
}
