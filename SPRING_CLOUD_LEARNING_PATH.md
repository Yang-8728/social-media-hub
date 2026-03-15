# Spring Cloud 学习路径 - 基于你的项目经验

## 🎯 学习目标

从你当前的 **Python 微服务项目** 过渡到 **Spring Cloud 企业级微服务**

---

## 📊 你的优势

✅ **已掌握的概念**（这些在 Spring Cloud 中是一样的）：
- ✅ 微服务架构思想
- ✅ 服务拆分原则（Standardizer、Merger、Downloader）
- ✅ API Gateway 概念
- ✅ Docker 容器化
- ✅ Redis 分布式缓存
- ✅ RESTful API 设计
- ✅ 异步任务处理

**这些经验让你比零基础学习者快 50%！**

---

## 🛤️ 学习路线图

```
第1阶段：Java 基础          (1-2周)  ← 如果已会 Java，跳过
   ↓
第2阶段：Spring Boot       (2-3周)  ← 核心基础
   ↓
第3阶段：Spring Cloud 核心  (3-4周)  ← 重点
   ↓
第4阶段：改造你的项目       (2-3周)  ← 实战
   ↓
第5阶段：企业级实践         (持续)   ← 进阶
```

**总时长：8-12 周完整掌握**

---

## 第1阶段：Java 基础准备（1-2周）

### 如果你已经会 Java
跳过此阶段，直接进入 Spring Boot

### 如果不熟悉 Java
**最小必学内容**（只学这些，够用了）：

```java
// 1. 基础语法（1天）
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello Spring Cloud");
    }
}

// 2. 面向对象（2天）
public class Video {
    private String filename;
    private String account;
    
    public Video(String filename, String account) {
        this.filename = filename;
        this.account = account;
    }
    
    // getter/setter
}

// 3. 集合框架（1天）
List<String> videos = new ArrayList<>();
Map<String, Object> config = new HashMap<>();

// 4. Lambda 表达式（1天）- Spring 常用
videos.stream()
      .filter(v -> v.endsWith(".mp4"))
      .forEach(System.out::println);
```

**推荐资源：**
- 视频：尚硅谷 Java 基础（只看前 30 集）
- 练习：在 IntelliJ IDEA 中写 100 行代码

**评估标准：**
- ✅ 能看懂 Java 代码
- ✅ 能写简单的类和方法
- ✅ 理解 List、Map 的使用

---

## 第2阶段：Spring Boot 核心（2-3周）

### 为什么先学 Spring Boot？
Spring Cloud 是建立在 Spring Boot 之上的，必须先掌握 Spring Boot。

### 学习内容

#### 第1周：Spring Boot 基础

**1. 创建第一个 Spring Boot 项目**
```bash
# 使用 Spring Initializr (https://start.spring.io/)
- Project: Maven
- Language: Java
- Spring Boot: 3.2.0
- Dependencies: Spring Web, Spring Data JPA, MySQL Driver
```

**2. Hello World REST API**
```java
@RestController
@RequestMapping("/api")
public class VideoController {
    
    @GetMapping("/videos")
    public List<Video> getVideos() {
        // 对比你的 Flask: @app.route('/videos')
        return Arrays.asList(
            new Video("video1.mp4", "ai_vanvan"),
            new Video("video2.mp4", "aigf8728")
        );
    }
    
    @PostMapping("/standardize")
    public ResponseEntity<?> standardize(@RequestBody StandardizeRequest request) {
        // 对比你的 Flask: @app.route('/standardize', methods=['POST'])
        return ResponseEntity.ok(Map.of("status", "processing"));
    }
}
```

**对比你的 Python 代码：**
| Python (Flask) | Java (Spring Boot) |
|----------------|-------------------|
| `@app.route('/videos')` | `@GetMapping("/videos")` |
| `request.get_json()` | `@RequestBody` |
| `jsonify(data)` | `ResponseEntity.ok(data)` |

**练习：**
- ✅ 创建一个视频管理 API
- ✅ 实现 CRUD 操作（增删改查）
- ✅ 连接 MySQL 数据库

---

#### 第2周：Spring Boot 进阶

**1. 依赖注入（核心概念）**
```java
// Python 中你是这样的：
# standardizer = Standardizer()
# merger = Merger(standardizer)  # 手动创建依赖

// Spring Boot 自动注入
@Service
public class StandardizerService {
    public void standardize(String video) {
        // 标准化逻辑
    }
}

@Service
public class MergerService {
    @Autowired  // Spring 自动注入
    private StandardizerService standardizer;
    
    public void merge(List<String> videos) {
        standardizer.standardize(videos.get(0));
        // 合并逻辑
    }
}
```

**2. 配置管理**
```yaml
# application.yml - 对比你的 config/accounts.json
server:
  port: 8080

app:
  video:
    download-path: /app/videos/downloads
    merge-path: /app/videos/merged
    
redis:
  host: localhost
  port: 6379
```

```java
@Service
public class VideoService {
    @Value("${app.video.download-path}")
    private String downloadPath;  // 自动读取配置
    
    @Autowired
    private RedisTemplate<String, Object> redisTemplate;  // 自动连接 Redis
}
```

**3. 异常处理**
```java
@ControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(VideoNotFoundException.class)
    public ResponseEntity<?> handleVideoNotFound(VideoNotFoundException e) {
        return ResponseEntity.status(404).body(Map.of("error", e.getMessage()));
    }
}
```

**练习：**
- ✅ 实现一个完整的视频处理服务
- ✅ 使用 Redis 缓存视频列表
- ✅ 添加全局异常处理

---

## 第3阶段：Spring Cloud 核心（3-4周）⭐

这是**重点阶段**，对应你的 API Gateway + 微服务架构。

### 第1周：服务注册与发现（Eureka）

**你的项目现状：**
```python
# API Gateway 硬编码服务地址
STANDARDIZER_URL = 'http://standardizer:8000'
MERGER_URL = 'http://merger:8000'
```

**Spring Cloud 方案：**

**1. 创建 Eureka Server（服务注册中心）**
```java
// eureka-server/src/main/java/EurekaServerApplication.java
@SpringBootApplication
@EnableEurekaServer  // ← 一个注解启动注册中心
public class EurekaServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(EurekaServerApplication.class, args);
    }
}
```

```yaml
# eureka-server/application.yml
server:
  port: 8761

eureka:
  client:
    register-with-eureka: false  # 注册中心自己不注册
    fetch-registry: false
```

**2. 改造 Standardizer 服务**
```java
// standardizer-service/src/main/java/StandardizerApplication.java
@SpringBootApplication
@EnableEurekaClient  // ← 自动注册到 Eureka
public class StandardizerApplication {
    public static void main(String[] args) {
        SpringApplication.run(StandardizerApplication.class, args);
    }
}
```

```yaml
# standardizer-service/application.yml
spring:
  application:
    name: standardizer-service  # ← 服务名

eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/  # 注册中心地址
```

**3. API Gateway 调用（自动发现）**
```java
@RestController
public class GatewayController {
    @Autowired
    private RestTemplate restTemplate;  // 自动负载均衡
    
    @PostMapping("/standardize")
    public ResponseEntity<?> standardize(@RequestBody Map<String, Object> request) {
        // 不再需要硬编码地址！
        return restTemplate.postForEntity(
            "http://standardizer-service/process",  // ← 使用服务名
            request,
            Map.class
        );
    }
}

@Configuration
public class RestTemplateConfig {
    @Bean
    @LoadBalanced  // ← 启用负载均衡
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
```

**Eureka 控制台：**
访问 http://localhost:8761
```
Instances currently registered with Eureka:
┌────────────────────┬────────┬────────────┐
│ Application        │ AMIs   │ Status     │
├────────────────────┼────────┼────────────┤
│ STANDARDIZER-SERVICE│ n/a (1)│ UP         │
│ MERGER-SERVICE     │ n/a (1)│ UP         │
│ API-GATEWAY        │ n/a (1)│ UP         │
└────────────────────┴────────┴────────────┘
```

**练习项目：**
创建一个简化版的你的项目：
- ✅ Eureka Server
- ✅ Standardizer Service（注册到 Eureka）
- ✅ Merger Service（注册到 Eureka）
- ✅ API Gateway（通过 Eureka 调用服务）

---

### 第2周：API Gateway（Spring Cloud Gateway）

**你的项目现状：**
```python
# containers/api-gateway/app.py
@app.route('/standardize-batch', methods=['POST'])
def start_standardize_batch():
    response = requests.post('http://standardizer:8000/process-batch', json=data)
    return jsonify(response.json())

@app.route('/merge', methods=['POST'])
def start_merge():
    response = requests.post('http://merger:8000/merge', json=data)
    return jsonify(response.json())
```

**Spring Cloud Gateway（配置驱动）：**
```yaml
# api-gateway/application.yml
spring:
  cloud:
    gateway:
      routes:
        # Standardizer 路由
        - id: standardizer-route
          uri: lb://standardizer-service  # lb = load balanced
          predicates:
            - Path=/api/standardize/**
          filters:
            - StripPrefix=1  # 去掉 /api 前缀
            
        # Merger 路由
        - id: merger-route
          uri: lb://merger-service
          predicates:
            - Path=/api/merge/**
          filters:
            - StripPrefix=1
            - name: CircuitBreaker
              args:
                name: mergerCircuitBreaker
                fallbackUri: forward:/fallback/merger
```

**高级功能：**
```yaml
# 限流
- name: RequestRateLimiter
  args:
    redis-rate-limiter.replenishRate: 10  # 每秒10个请求
    redis-rate-limiter.burstCapacity: 20

# 重试
- name: Retry
  args:
    retries: 3
    statuses: BAD_GATEWAY
```

**练习：**
- ✅ 配置所有服务的路由
- ✅ 添加限流保护
- ✅ 实现重试机制

---

### 第3周：配置中心（Config Server）

**你的项目现状：**
```
containers/
  standardizer/.env
  merger/.env
  api-gateway/.env
每个服务独立配置，修改需要重启
```

**Spring Cloud Config：**

**1. 创建 Config Server**
```java
@SpringBootApplication
@EnableConfigServer
public class ConfigServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(ConfigServerApplication.class, args);
    }
}
```

```yaml
# config-server/application.yml
spring:
  cloud:
    config:
      server:
        git:
          uri: https://github.com/your-name/config-repo  # Git 仓库
          default-label: main
```

**2. Git 仓库配置**
```
config-repo/
  application.yml          # 所有服务共享
  standardizer-dev.yml     # Standardizer 开发环境
  standardizer-prod.yml    # Standardizer 生产环境
  merger-dev.yml
  merger-prod.yml
```

```yaml
# application.yml
redis:
  host: redis-server
  port: 6379

logging:
  level:
    root: INFO
```

```yaml
# standardizer-prod.yml
app:
  video:
    max-workers: 8
    output-quality: high
```

**3. 服务使用配置**
```yaml
# standardizer-service/bootstrap.yml
spring:
  application:
    name: standardizer
  profiles:
    active: prod
  cloud:
    config:
      uri: http://config-server:8888  # Config Server 地址
```

**动态刷新配置（无需重启）：**
```java
@RestController
@RefreshScope  // ← 支持动态刷新
public class VideoController {
    @Value("${app.video.max-workers}")
    private int maxWorkers;  // 配置更新后自动刷新
}
```

```bash
# 刷新配置
curl -X POST http://standardizer-service:8080/actuator/refresh
```

**练习：**
- ✅ 搭建 Config Server
- ✅ 将所有服务配置迁移到 Git
- ✅ 实现配置动态刷新

---

### 第4周：断路器（Resilience4j）

**你的项目现状：**
```python
# 服务挂了就直接失败
try:
    response = requests.post('http://standardizer:8000/process', timeout=10)
except Exception:
    return jsonify({'error': 'Service unavailable'}), 500
```

**Spring Cloud 断路器：**
```java
@RestController
public class VideoController {
    @Autowired
    private StandardizerClient standardizerClient;
    
    @GetMapping("/standardize/{id}")
    @CircuitBreaker(name = "standardizer", fallbackMethod = "standardizeFallback")
    @RateLimiter(name = "standardizer")
    @Retry(name = "standardizer")
    public ResponseEntity<?> standardize(@PathVariable String id) {
        return standardizerClient.process(id);
    }
    
    // 降级方法
    public ResponseEntity<?> standardizeFallback(String id, Exception e) {
        return ResponseEntity.ok(Map.of(
            "message", "Standardizer service is temporarily unavailable",
            "videoId", id,
            "fallback", true
        ));
    }
}
```

**配置：**
```yaml
# application.yml
resilience4j:
  circuitbreaker:
    instances:
      standardizer:
        sliding-window-size: 10
        failure-rate-threshold: 50  # 50% 失败率触发断路器
        wait-duration-in-open-state: 10000  # 10秒后尝试恢复
        
  retry:
    instances:
      standardizer:
        max-attempts: 3
        wait-duration: 1000
        
  ratelimiter:
    instances:
      standardizer:
        limit-for-period: 10  # 每秒10个请求
        timeout-duration: 0
```

**监控断路器状态：**
```java
// 访问 /actuator/health
{
  "status": "UP",
  "circuitBreakers": {
    "standardizer": "CLOSED"  // CLOSED/OPEN/HALF_OPEN
  }
}
```

**练习：**
- ✅ 为所有服务调用添加断路器
- ✅ 配置重试策略
- ✅ 实现降级逻辑
- ✅ 测试服务故障场景

---

## 第4阶段：改造你的项目（2-3周）⭐

### 项目：社交媒体自动化平台 - Spring Cloud 版

**架构对比：**

```
【Python 版】
API Gateway (Flask)
  ↓
├─ Standardizer (Flask)
├─ Merger (FastAPI)
├─ Downloader (Flask)
└─ Uploader (Flask)

【Spring Cloud 版】
Eureka Server (8761)
  ↓
API Gateway (Spring Cloud Gateway, 8080)
  ↓
├─ Standardizer Service (8001)
├─ Merger Service (8002)
├─ Downloader Service (8003)
└─ Uploader Service (8004)
```

### 第1周：搭建基础框架

**1. 创建父项目**
```xml
<!-- pom.xml -->
<project>
    <groupId>com.socialmedia</groupId>
    <artifactId>social-media-hub</artifactId>
    <version>1.0.0</version>
    <packaging>pom</packaging>
    
    <modules>
        <module>eureka-server</module>
        <module>api-gateway</module>
        <module>standardizer-service</module>
        <module>merger-service</module>
        <module>downloader-service</module>
        <module>uploader-service</module>
    </modules>
</project>
```

**2. 创建各个模块**
```
social-media-hub/
├── eureka-server/
│   └── src/main/java/.../EurekaServerApplication.java
├── api-gateway/
│   └── src/main/java/.../ApiGatewayApplication.java
├── standardizer-service/
│   ├── src/main/java/.../
│   │   ├── StandardizerApplication.java
│   │   ├── controller/VideoController.java
│   │   ├── service/StandardizerService.java
│   │   └── config/RedisConfig.java
│   └── src/main/resources/application.yml
└── merger-service/
    └── ...
```

---

### 第2周：实现核心功能

**Standardizer Service：**
```java
@RestController
@RequestMapping("/api/videos")
public class VideoController {
    @Autowired
    private StandardizerService standardizerService;
    
    @PostMapping("/standardize")
    public ResponseEntity<?> standardize(@RequestBody StandardizeRequest request) {
        String taskId = standardizerService.startStandardize(
            request.getAccount(),
            request.getVideoFiles(),
            request.getProcessType()
        );
        
        return ResponseEntity.ok(Map.of(
            "message", "Standardization started",
            "taskId", taskId
        ));
    }
    
    @GetMapping("/status/{taskId}")
    public ResponseEntity<?> getStatus(@PathVariable String taskId) {
        TaskStatus status = standardizerService.getStatus(taskId);
        return ResponseEntity.ok(status);
    }
}

@Service
public class StandardizerService {
    @Autowired
    private RedisTemplate<String, Object> redisTemplate;
    
    @Async  // 异步处理
    public String startStandardize(String account, List<String> files, String type) {
        String taskId = UUID.randomUUID().toString();
        
        // 调用 FFmpeg（可以用 ProcessBuilder 或 JNI）
        // 对比你的 Python: subprocess.run(['ffmpeg', ...])
        ProcessBuilder pb = new ProcessBuilder(
            "ffmpeg", "-i", inputFile, "-c:v", "libx264", outputFile
        );
        Process process = pb.start();
        
        // 保存任务状态到 Redis
        redisTemplate.opsForValue().set("task:" + taskId, status);
        
        return taskId;
    }
}
```

**Merger Service：**
```java
@RestController
@RequestMapping("/api/merge")
public class MergerController {
    @Autowired
    private MergerService mergerService;
    
    @PostMapping
    public ResponseEntity<?> merge(@RequestBody MergeRequest request) {
        MergeResult result = mergerService.mergeVideos(
            request.getAccount(),
            request.getLimit()
        );
        
        return ResponseEntity.ok(result);
    }
}

@Service
public class MergerService {
    @Autowired
    private StandardizerClient standardizerClient;  // Feign 客户端
    
    public MergeResult mergeVideos(String account, Integer limit) {
        // 调用 Standardizer 获取标准化视频
        List<Video> videos = standardizerClient.getStandardizedVideos(account);
        
        // 合并逻辑（FFmpeg）
        // ...
        
        return new MergeResult(outputFile, videos.size());
    }
}
```

**Feign 客户端（服务间调用）：**
```java
@FeignClient(name = "standardizer-service")
public interface StandardizerClient {
    @GetMapping("/api/videos/standardized/{account}")
    List<Video> getStandardizedVideos(@PathVariable String account);
}
```

---

### 第3周：完善和测试

**1. Docker 部署**
```yaml
# docker-compose.yml
version: '3.8'
services:
  eureka-server:
    build: ./eureka-server
    ports:
      - "8761:8761"
      
  api-gateway:
    build: ./api-gateway
    ports:
      - "8080:8080"
    depends_on:
      - eureka-server
      
  standardizer:
    build: ./standardizer-service
    deploy:
      replicas: 2  # 两个实例
    depends_on:
      - eureka-server
      - redis
      
  merger:
    build: ./merger-service
    depends_on:
      - eureka-server
      - redis
      
  redis:
    image: redis:alpine
```

**2. 测试**
```bash
# 启动所有服务
docker-compose up -d

# 查看 Eureka
open http://localhost:8761

# 测试 API
curl -X POST http://localhost:8080/api/videos/standardize \
  -H "Content-Type: application/json" \
  -d '{
    "account": "ai_vanvan",
    "videoFiles": ["video1.mp4", "video2.mp4"],
    "processType": "ultimate"
  }'
```

**3. 监控**
```yaml
# application.yml - 所有服务添加
management:
  endpoints:
    web:
      exposure:
        include: "*"
  metrics:
    export:
      prometheus:
        enabled: true
```

访问监控端点：
- http://localhost:8080/actuator/health
- http://localhost:8080/actuator/metrics
- http://localhost:8080/actuator/prometheus

---

## 第5阶段：企业级实践（持续学习）

### 1. 链路追踪（Sleuth + Zipkin）

**添加依赖：**
```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-sleuth</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-sleuth-zipkin</artifactId>
</dependency>
```

**配置：**
```yaml
spring:
  sleuth:
    sampler:
      probability: 1.0  # 100% 采样
  zipkin:
    base-url: http://zipkin-server:9411
```

**启动 Zipkin：**
```bash
docker run -d -p 9411:9411 openzipkin/zipkin
```

访问 http://localhost:9411 查看调用链。

---

### 2. 统一认证（OAuth2 + JWT）

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.oauth2ResourceServer()
            .jwt();
    }
}
```

---

### 3. 消息驱动（Spring Cloud Stream）

```java
@Service
public class VideoProcessingService {
    @Autowired
    private StreamBridge streamBridge;
    
    public void processVideo(Video video) {
        // 发送消息到 Kafka/RabbitMQ
        streamBridge.send("video-processed", video);
    }
}

@Component
public class VideoConsumer {
    @StreamListener("video-processed")
    public void handleProcessedVideo(Video video) {
        // 处理消息
    }
}
```

---

## 📚 推荐学习资源

### 官方文档
- Spring Boot: https://spring.io/projects/spring-boot
- Spring Cloud: https://spring.io/projects/spring-cloud

### 视频教程
1. **尚硅谷 Spring Cloud 教程**（免费，B站）
   - 全面系统，适合初学者
   - 配套代码和笔记

2. **黑马程序员 Spring Cloud 微服务**
   - 项目驱动，实战性强

### 书籍
1. **《Spring Cloud 微服务实战》** - 翟永超
2. **《Spring Cloud Alibaba 微服务原理与实战》**

### 实战项目
1. **mall** (GitHub 10w+ stars)
   - https://github.com/macrozheng/mall
   - 电商系统，Spring Cloud 全家桶
   
2. **pig** (开源后台管理系统)
   - https://gitee.com/log4j/pig
   - 权限管理、微服务架构

---

## 🎯 学习建议

### 1. 边学边对照你的项目
```
学习 Eureka → 思考：我的 API Gateway 如何改造？
学习 Config Server → 思考：我的配置文件如何迁移？
学习断路器 → 思考：我的错误处理可以如何改进？
```

### 2. 动手比看视频重要
- ❌ 只看教程，不写代码
- ✅ 每学一个组件，立即实践
- ✅ 改造你的项目一小部分

### 3. 循序渐进
```
第1个月：理解概念，能运行 Demo
第2个月：独立搭建简单项目
第3个月：改造你的项目
第4个月：添加高级特性
```

### 4. 面试准备
重点掌握：
- ✅ 服务注册与发现原理
- ✅ 负载均衡策略
- ✅ 断路器工作机制
- ✅ 配置中心优势
- ✅ 微服务拆分原则
- ✅ 分布式事务处理

---

## 🚀 3个月后你能达到的水平

**技术栈：**
- ✅ Spring Boot + Spring Cloud 全家桶
- ✅ Eureka/Nacos 服务注册
- ✅ Gateway API 网关
- ✅ Feign 服务调用
- ✅ Hystrix/Resilience4j 熔断降级
- ✅ Config 配置中心
- ✅ Sleuth + Zipkin 链路追踪

**项目经验：**
- ✅ 社交媒体自动化平台（Spring Cloud 版）
- ✅ 理解微服务架构设计
- ✅ 能独立搭建企业级微服务

**简历亮点：**
```
项目：社交媒体内容管理平台（Spring Cloud 微服务架构）
技术栈：
- 使用 Spring Cloud Netflix Eureka 实现服务注册与发现
- 基于 Spring Cloud Gateway 构建 API 网关，实现统一鉴权和限流
- 采用 Resilience4j 实现服务熔断、降级和重试机制
- 集成 Spring Cloud Config 实现配置中心，支持配置动态刷新
- 使用 Feign 实现声明式服务调用
- 通过 Sleuth + Zipkin 实现分布式链路追踪
- Docker 容器化部署，支持服务快速扩展

亮点：
- 从零到一搭建微服务架构
- 服务高可用设计（负载均衡 + 熔断降级）
- 性能优化（Redis 缓存 + 异步处理）
```

---

## 📝 学习计划表

### 第1-2周：Spring Boot 基础
- [ ] 搭建 Spring Boot 项目
- [ ] 实现 RESTful API
- [ ] 集成 Redis
- [ ] 集成 MySQL

### 第3-4周：Eureka + Gateway
- [ ] 搭建 Eureka Server
- [ ] 创建 2 个微服务并注册
- [ ] 配置 Spring Cloud Gateway
- [ ] 实现服务调用

### 第5-6周：Config + Resilience4j
- [ ] 搭建 Config Server
- [ ] 配置动态刷新
- [ ] 实现断路器
- [ ] 添加重试和限流

### 第7-8周：改造你的项目
- [ ] 创建 Standardizer Service
- [ ] 创建 Merger Service
- [ ] 实现 Feign 服务调用
- [ ] Docker 部署

### 第9-12周：进阶和完善
- [ ] 添加链路追踪
- [ ] 实现统一认证
- [ ] 性能监控
- [ ] 准备面试

---

## ⚠️ 常见坑点

### 1. 版本兼容性
```xml
<!-- Spring Boot 和 Spring Cloud 版本必须匹配 -->
<spring-boot.version>3.2.0</spring-boot.version>
<spring-cloud.version>2023.0.0</spring-cloud.version>
```

### 2. 端口冲突
确保每个服务使用不同端口：
- Eureka Server: 8761
- API Gateway: 8080
- Service A: 8001
- Service B: 8002

### 3. Eureka 注册慢
```yaml
eureka:
  instance:
    lease-renewal-interval-in-seconds: 5  # 心跳间隔
    lease-expiration-duration-in-seconds: 10  # 过期时间
```

---

## 💡 最后的建议

1. **不要完全放弃 Python 项目**
   - Python 版本作为快速原型
   - Spring Cloud 版本作为企业级实现
   - 两者对比学习效果更好

2. **加入社区**
   - Spring Cloud 中文社区
   - GitHub 开源项目
   - 技术博客（掘金、CSDN）

3. **准备笔记**
   - 记录踩坑经历
   - 整理成博客
   - 面试时能清晰表达

4. **参与开源**
   - 给开源项目提 PR
   - 增加 GitHub 贡献
   - 提升简历竞争力

---

**祝你学习顺利！3个月后你将掌握企业级微服务开发！** 🚀

有任何问题随时问我！
