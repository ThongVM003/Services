deploy-kafka-full:
	@docker compose -f docker-compose.yml up -d

deploy-kafka-standalone:
	@docker compose -f docker-compose.yml up broker -d

deploy-kafka-old:
	@docker compose -f old-pose.yml up -d 

run-test-image:
	@docker compose -f "./scripts/docker-compose.yml" up -d --build