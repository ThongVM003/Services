# ============================
# Run Services
# ============================

# Commands to start individual services
run-portainer:
	@docker compose -f portainer/docker-compose.yml up portainer -d

run-portainer-agent:
	@docker compose -f portainer/docker-compose.yml up portainer-agent -d

run-kafka-broker:
	@docker compose -f kafka/docker-compose.yml up broker -d

run-kafka-all:
	@docker compose -f kafka/docker-compose.yml up -d

run-milvus-all:
	@docker compose -f milvus/docker-compose.yml up -d

run-minio:
	@docker compose -f minio/docker-compose.yml up -d

run-mongodb:
	@docker compose -f mongodb/docker-compose.yml up -d

run-redis:
	@docker compose -f redis/docker-compose.yml up -d

# Command to start all services
run-all: run-portainer run-portainer-agent run-kafka-broker run-kafka-all run-milvus-all run-minio run-mongodb run-redis


# ============================
# Update Services
# ============================

# Commands to update individual services with the latest images
update-portainer:
	@docker compose -f portainer/docker-compose.yml up portainer -d --pull always

update-portainer-agent:
	@docker compose -f portainer/docker-compose.yml up portainer-agent -d --pull always

update-kafka-broker:
	@docker compose -f kafka/docker-compose.yml up broker -d --pull always

update-kafka-all:
	@docker compose -f kafka/docker-compose.yml up -d --pull always

update-milvus-all:
	@docker compose -f milvus/docker-compose.yml up -d --pull always

update-minio:
	@docker compose -f minio/docker-compose.yml up -d --pull always

update-mongodb:
	@docker compose -f mongodb/docker-compose.yml up -d --pull always

update-redis:
	@docker compose -f redis/docker-compose.yml up -d --pull always

# Command to update all services
update-all: update-portainer update-portainer-agent update-kafka-broker update-kafka-all update-milvus-all update-minio update-mongodb update-redis


# ============================
# Stop Services
# ============================

# Commands to stop individual services
stop-portainer:
	@docker compose -f portainer/docker-compose.yml stop portainer

stop-portainer-agent:
	@docker compose -f portainer/docker-compose.yml stop portainer-agent

stop-kafka-broker:
	@docker compose -f kafka/docker-compose.yml stop broker

stop-kafka-all:
	@docker compose -f kafka/docker-compose.yml stop

stop-milvus-all:
	@docker compose -f milvus/docker-compose.yml stop

stop-minio:
	@docker compose -f minio/docker-compose.yml stop

stop-mongodb:
	@docker compose -f mongodb/docker-compose.yml stop

stop-redis:
	@docker compose -f redis/docker-compose.yml stop

# Command to stop all services
stop-all: stop-portainer stop-portainer-agent stop-kafka-broker stop-kafka-all stop-milvus-all stop-minio stop-mongodb stop-redis


# ============================
# Restart Services
# ============================

# Commands to restart individual services
restart-portainer:
	@docker compose -f portainer/docker-compose.yml restart portainer

restart-portainer-agent:
	@docker compose -f portainer/docker-compose.yml restart portainer-agent

restart-kafka-broker:
	@docker compose -f kafka/docker-compose.yml restart broker

restart-kafka-all:
	@docker compose -f kafka/docker-compose.yml restart

restart-milvus-all:
	@docker compose -f milvus/docker-compose.yml restart

restart-minio:
	@docker compose -f minio/docker-compose.yml restart

restart-mongodb:
	@docker compose -f mongodb/docker-compose.yml restart

restart-redis:
	@docker compose -f redis/docker-compose.yml restart

# Command to restart all services
restart-all: restart-portainer restart-portainer-agent restart-kafka-broker restart-kafka-all restart-milvus-all restart-minio restart-mongodb restart-redis


# ============================
# Logs
# ============================

# Commands to view logs for individual services
logs-portainer:
	@docker compose -f portainer/docker-compose.yml logs -f --tail 1000 portainer

logs-portainer-agent:
	@docker compose -f portainer/docker-compose.yml logs -f --tail 1000 portainer-agent

logs-kafka-broker:
	@docker compose -f kafka/docker-compose.yml logs -f --tail 1000 broker

logs-kafka-all:
	@docker compose -f kafka/docker-compose.yml logs -f --tail 1000

logs-milvus-all:
	@docker compose -f milvus/docker-compose.yml logs -f --tail 1000

logs-minio:
	@docker compose -f minio/docker-compose.yml logs -f --tail 1000

logs-mongodb:
	@docker compose -f mongodb/docker-compose.yml logs -f --tail 1000

logs-redis:
	@docker compose -f redis/docker-compose.yml logs -f --tail 1000

# Command to view logs for all services
logs-all: logs-portainer logs-portainer-agent logs-kafka-broker logs-kafka-all logs-milvus-all logs-minio logs-mongodb logs-redis


# ============================
# Remove Services
# ============================

# Commands to remove individual services
rm-portainer:
	@docker compose -f portainer/docker-compose.yml down portainer

rm-portainer-agent:
	@docker compose -f portainer/docker-compose.yml down portainer-agent

rm-kafka-broker:
	@docker compose -f kafka/docker-compose.yml down broker

rm-kafka-all:
	@docker compose -f kafka/docker-compose.yml down

rm-milvus-all:
	@docker compose -f milvus/docker-compose.yml down

rm-minio:
	@docker compose -f minio/docker-compose.yml down

rm-mongodb:
	@docker compose -f mongodb/docker-compose.yml down

rm-redis:
	@docker compose -f redis/docker-compose.yml down

# Command to remove all services
rm-all: rm-portainer rm-portainer-agent rm-kafka-broker rm-kafka-all rm-milvus-all rm-minio rm-mongodb rm-redis