const { createClient } = require('redis');
const { createClient as createPgClient } = require('pg');
const { v4: uuidv4 } = require('uuid');
const { promisify } = require('util');

class Parser {
  constructor(pgClient, redisClient) {
    this.pgClient = pgClient;
    this.redisClient = redisClient;
  }

  async parseAuthenticationRequest(data) {
    const { username, password } = data;
    const token = uuidv4();

    await this.pgClient.query('INSERT INTO users (username, password) VALUES ($1, $2)', [username, password]);

    await this.redisClient.set(token, JSON.stringify(data));

    return token;
  }

  async parseAuthenticationResponse(token) {
    const data = await this.redisClient.get(token);

    if (!data) {
      return null;
    }

    const parsedData = JSON.parse(data);

    return parsedData;
  }
}

const createPgClientAsync = promisify(createPgClient).bind(null);
const createRedisClientAsync = promisify(createClient).bind(null);

async function main() {
  const pgClient = await createPgClientAsync('postgresql://localhost:5432/auth_gateway');
  const redisClient = await createRedisClientAsync({ host: 'localhost', port: 6379 });

  const parser = new Parser(pgClient, redisClient);

  const token = await parser.parseAuthenticationRequest({ username: 'user1', password: 'password1' });

  const parsedData = await parser.parseAuthenticationResponse(token);

  console.log(parsedData);
}

main();