import { error, json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

const API_BASE = 'http://localhost:8000';

export const GET: RequestHandler = async ({ params, fetch }) => {
    try {
        const response = await fetch(`${API_BASE}/products/${params.id}`);
        
        if (!response.ok) {
            if (response.status === 404) {
                throw error(404, 'Product not found');
            }
            throw error(response.status, 'Failed to fetch product');
        }

        const product = await response.json();
        return json({
            ...product,
            image: `https://picsum.photos/seed/${product.id}/600/400`,
            description: `${product.name} - Stock: ${product.stock} units`
        });
    } catch (e) {
        console.error('Error fetching product:', e);
        throw error(500, 'Internal Server Error');
    }
};

export const PUT: RequestHandler = async ({ params, request, fetch }) => {
    try {
        const product = await request.json();
        
        const response = await fetch(`${API_BASE}/products/${params.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(product),
        });

        if (!response.ok) {
            if (response.status === 404) {
                throw error(404, 'Product not found');
            }
            throw error(response.status, 'Failed to update product');
        }

        const updatedProduct = await response.json();
        return json(updatedProduct);
    } catch (e) {
        console.error('Error updating product:', e);
        throw error(500, 'Internal Server Error');
    }
};

export const DELETE: RequestHandler = async ({ params, fetch }) => {
    try {
        const response = await fetch(`${API_BASE}/products/${params.id}`, {
            method: 'DELETE',
        });

        if (!response.ok) {
            if (response.status === 404) {
                throw error(404, 'Product not found');
            }
            throw error(response.status, 'Failed to delete product');
        }

        return json({ message: 'Product deleted successfully' });
    } catch (e) {
        console.error('Error deleting product:', e);
        throw error(500, 'Internal Server Error');
    }
};
