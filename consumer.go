package main

import (
	"context"
	"fmt"
	"github.com/Shopify/sarama"
	"log"
	"os"
	"os/signal"
	"syscall"
)

func main() {
	// 创建Sarama消费者配置
	config := sarama.NewConfig()
	config.Net.SASL.Enable = true
	config.Net.SASL.User = "xxxxx"
	config.Net.SASL.Password = "xxxxx"
	config.Net.SASL.Mechanism = sarama.SASLTypePlaintext
	config.Consumer.Group.Rebalance.Strategy = sarama.BalanceStrategyRoundRobin
	config.Version = sarama.V1_1_1_0
	config.Consumer.Offsets.Initial = sarama.OffsetNewest

	// 创建Sarama消费者
	sarama.Logger = log.New(os.Stdout, "[Sarama] ", log.LstdFlags)
	consumer, err := sarama.NewConsumerGroup([]string{"xxxx_broker_addr"}, "xxxx_group_id", config)
	if err != nil {
		log.Fatal(err)
	}
	defer consumer.Close()

	// 处理接收到的消息
	handler := &ConsumerGroupHandler{}
	signals := make(chan os.Signal, 1)
	signal.Notify(signals, syscall.SIGINT, syscall.SIGTERM)

	go func() {
		for {
			err := consumer.Consume(context.Background(), []string{"xxxxxxx_topic_name"}, handler)
			if err != nil {
				log.Fatal(err)
			}
			if handler.ready {
				break
			}
		}
	}()

	<-signals
	fmt.Println("Exiting...")
}

// ConsumerGroupHandler 实现了sarama.ConsumerGroupHandler接口
type ConsumerGroupHandler struct {
	ready bool
}

// Setup 在消费者组启动之前调用
func (h *ConsumerGroupHandler) Setup(sarama.ConsumerGroupSession) error {
	h.ready = true
	return nil
}

// Cleanup 在消费者组停止之后调用
func (h *ConsumerGroupHandler) Cleanup(sarama.ConsumerGroupSession) error {
	h.ready = false
	return nil
}

// ConsumeClaim 消费Claim中的消息
func (h *ConsumerGroupHandler) ConsumeClaim(session sarama.ConsumerGroupSession, claim sarama.ConsumerGroupClaim) error {
	for message := range claim.Messages() {
		fmt.Printf("Received message: %s\n", string(message.Value))
		session.MarkMessage(message, "")
	}
	return nil
}
