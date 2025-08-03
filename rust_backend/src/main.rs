use axum::{
    http::StatusCode,
    response::Json,
    routing::get,
    Router,
};
use serde::{Deserialize, Serialize};
use tower_http::cors::{Any, CorsLayer};
use tracing::info;

#[derive(Serialize, Deserialize)]
struct HealthResponse {
    status: String,
    message: String,
    timestamp: String,
}

#[derive(Serialize, Deserialize)]
struct Property {
    id: u32,
    title: String,
    description: String,
    price: f64,
    location: String,
    property_type: String,
    status: String,
}

#[derive(Serialize, Deserialize)]
struct User {
    id: u32,
    name: String,
    email: String,
    role: String,
}

async fn health_check() -> Json<HealthResponse> {
    info!("Health check endpoint called");
    Json(HealthResponse {
        status: "ok".to_string(),
        message: "Rust backend is running".to_string(),
        timestamp: chrono::Utc::now().to_rfc3339(),
    })
}

async fn get_properties() -> Json<Vec<Property>> {
    info!("Get properties endpoint called");
    // Mock data - em produção viria do banco de dados
    let properties = vec![
        Property {
            id: 1,
            title: "Casa Moderna".to_string(),
            description: "Linda casa com 3 quartos".to_string(),
            price: 450000.0,
            location: "São Paulo, SP".to_string(),
            property_type: "Casa".to_string(),
            status: "Disponível".to_string(),
        },
        Property {
            id: 2,
            title: "Apartamento Centro".to_string(),
            description: "Apartamento no centro da cidade".to_string(),
            price: 320000.0,
            location: "Rio de Janeiro, RJ".to_string(),
            property_type: "Apartamento".to_string(),
            status: "Vendido".to_string(),
        },
    ];
    Json(properties)
}

async fn get_users() -> Json<Vec<User>> {
    info!("Get users endpoint called");
    // Mock data - em produção viria do banco de dados
    let users = vec![
        User {
            id: 1,
            name: "João Silva".to_string(),
            email: "joao@email.com".to_string(),
            role: "Admin".to_string(),
        },
        User {
            id: 2,
            name: "Maria Santos".to_string(),
            email: "maria@email.com".to_string(),
            role: "User".to_string(),
        },
    ];
    Json(users)
}

#[tokio::main]
async fn main() {
    // Inicializar logging
    tracing_subscriber::fmt::init();

    // Configurar CORS
    let cors = CorsLayer::new()
        .allow_origin(Any)
        .allow_methods(Any)
        .allow_headers(Any);

    // Criar rotas
    let app = Router::new()
        .route("/api/v1/health", get(health_check))
        .route("/api/v1/properties", get(get_properties))
        .route("/api/v1/users", get(get_users))
        .layer(cors);

    // Iniciar servidor
    let listener = tokio::net::TcpListener::bind("0.0.0.0:8080").await.unwrap();
    info!("🚀 Servidor Rust rodando em http://localhost:8080");
    info!("📋 Endpoints disponíveis:");
    info!("   GET /api/v1/health");
    info!("   GET /api/v1/properties");
    info!("   GET /api/v1/users");

    axum::serve(listener, app).await.unwrap();
 
}
