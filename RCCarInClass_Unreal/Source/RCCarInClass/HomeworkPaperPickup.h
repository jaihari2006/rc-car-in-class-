#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HomeworkPaperPickup.generated.h"

class USphereComponent;
class UStaticMeshComponent;
class URotatingMovementComponent;

UCLASS()
class RCCARINCLASS_API AHomeworkPaperPickup : public AActor
{
	GENERATED_BODY()

public:
	AHomeworkPaperPickup();

	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Pickup | Collision")
	USphereComponent* CollisionSphere;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Pickup | Mesh")
	UStaticMeshComponent* PaperMesh;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Pickup | Movement")
	URotatingMovementComponent* RotatingMovement;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Pickup | Rewards")
	int32 PointValue = 100;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Pickup | Rewards")
	int32 CoinValue = 25;

	UFUNCTION()
	void OnOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor,
	                    UPrimitiveComponent* OtherComp, int32 OtherBodyIndex,
	                    bool bFromSweep, const FHitResult& SweepResult);
};
