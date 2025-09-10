import { error, json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

const API_BASE = 'http://localhost:8000';

export const GET: RequestHandler = async ({ fetch }) => {
    try {
        const response = await fetch(`${API_BASE}/products/`);
        
        if (!response.ok) {
            throw error(response.status, 'Failed to fetch products');
        }

        const products = await response.json();
        return json(products.map((product: any) => ({
            ...product,
            image: `https://picsum.photos/seed/${product.id}/300/200`,
            description: `${product.name} - Stock: ${product.stock} units`
        })));
    } catch (e) {
        console.error('Error fetching products:', e);
        throw error(500, 'Internal Server Error');
    }
};

export const POST: RequestHandler = async ({ request, fetch }) => {
    try {
        const product = await request.json();
        
        const response = await fetch(`${API_BASE}/products/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(product),
        });

        if (!response.ok) {
            throw error(response.status, 'Failed to create product');
        }

        const newProduct = await response.json();
        return json(newProduct);
    } catch (e) {
        console.error('Error creating product:', e);
        throw error(500, 'Internal Server Error');
    }
};
