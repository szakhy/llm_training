<script lang="ts">
    import { onMount } from 'svelte';
    
    import type { Product } from '$lib/types';

    let products: Product[] = [];
    let loading = true;
    let error: string | null = null;

    async function fetchProducts() {
        try {
            const res = await fetch('/products');
            if (!res.ok) throw new Error('Failed to fetch products');
            products = await res.json();
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
            console.error('Error fetching products:', e);
        } finally {
            loading = false;
        }
    }

    onMount(fetchProducts);
</script>

<div class="container">
    <nav>
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/products">Products</a></li>
        </ul>
    </nav>

    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h1>Featured Products</h1>
        <div class="add-new"><a href="/products/new">Add New Product</a></div>
    </div>
        
    {#if loading}
        <div style="text-align: center; padding: 20px;">
            Loading...
        </div>
    {:else if error}
        <div style="color: red; border: 1px solid red; padding: 10px; margin: 10px 0;">
            {error}
        </div>
    {:else if products.length === 0}
        <div style="text-align: center; padding: 20px;">
            No products available.
        </div>
    {:else}
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Product Name</th>
                    <th>Price</th>
                    <th>Stock</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {#each products as product}
                    <tr>
                        <td>{product.id}</td>
                        <td>{product.name}</td>
                        <td>${product.price.toFixed(2)}</td>
                        <td>{product.stock} units</td>
                        <td>
                            <a href="/products/{product.id}" class="view-link">View</a>
                        </td>
                    </tr>
                {/each}
            </tbody>
        </table>
    {/if}
</div>
