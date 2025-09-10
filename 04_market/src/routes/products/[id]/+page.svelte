<script lang="ts">
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import type { Product } from '$lib/types';

    let product: Product | null = null;
    let loading = true;
    let error: string | null = null;
    let showEditModal = false;
    let editingProduct: { name: string; price: number; stock: number } = {
        name: '',
        price: 0,
        stock: 0
    };

    async function fetchProduct() {
        loading = true;
        error = null;
        try {
            const res = await fetch(`/products/${$page.params.id}`);
            if (!res.ok) {
                if (res.status === 404) {
                    error = 'Product not found';
                    return;
                }
                throw new Error('Failed to fetch product details');
            }
            product = await res.json();
            // Initialize editing form with current values
            if (product) {
                editingProduct = {
                    name: product.name,
                    price: product.price,
                    stock: product.stock
                };
            }
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        } finally {
            loading = false;
        }
    }

    async function updateProduct() {
        try {
            const res = await fetch(`/products/${$page.params.id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: editingProduct.name,
                    price: editingProduct.price,
                    stock: editingProduct.stock
                }),
            });

            if (!res.ok) throw new Error('Failed to update product');
            
            await fetchProduct();
            showEditModal = false;
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        }
    }

    onMount(fetchProduct);
</script>

<div class="container">
    <nav>
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/products">Products</a></li>
            <li>{product?.name || 'Loading...'}</li>
        </ul>
    </nav>

    {#if loading}
        <div style="text-align: center; padding: 20px;">
            Loading...
        </div>
    {:else if error}
        <div style="color: red; border: 1px solid red; padding: 10px; margin: 10px 0;">
            {error}
        </div>
    {:else if product}
        <div>
            <div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <h1>{product.name}</h1>
                    <button on:click={() => {
                        if (product) {
                            editingProduct = {
                                name: product.name,
                                price: product.price,
                                stock: product.stock
                            };
                            showEditModal = true;
                        }
                    }}>
                        Edit Product
                    </button>
                </div>
                
                <table>
                    <thead>
                        <tr>
                            <th>Property</th>
                            <th>Value</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>ID</td>
                            <td>{product.id}</td>
                        </tr>
                        <tr>
                            <td>Name</td>
                            <td>{product.name}</td>
                        </tr>
                        <tr>
                            <td>Price</td>
                            <td>${product.price.toFixed(2)}</td>
                        </tr>
                        <tr>
                            <td>Stock</td>
                            <td>{product.stock} units</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        {#if showEditModal}
        <div style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center;">
            <div style="background: white; padding: 20px; border-radius: 5px; width: 300px;">
                <h3 style="margin-top: 0;">Edit Product</h3>
                <form on:submit|preventDefault={updateProduct}>
                    <div style="margin-bottom: 10px;">
                        <label for="edit-name">Product Name</label>
                        <input id="edit-name" required bind:value={editingProduct.name} style="width: 100%; padding: 5px;" />
                    </div>
                    <div style="margin-bottom: 10px;">
                        <label for="edit-price">Price</label>
                        <input id="edit-price" type="number" step="0.01" required bind:value={editingProduct.price} style="width: 100%; padding: 5px;" />
                    </div>
                    <div style="margin-bottom: 10px;">
                        <label for="edit-stock">Stock</label>
                        <input id="edit-stock" type="number" required bind:value={editingProduct.stock} style="width: 100%; padding: 5px;" />
                    </div>
                    <div style="display: flex; justify-content: flex-end; gap: 10px;">
                        <button type="button" on:click={() => showEditModal = false}>Cancel</button>
                        <button type="submit" style="background-color: blue; color: white;">Save Changes</button>
                    </div>
                </form>
            </div>
        </div>
        {/if}
    {:else}
        <p>Product not found.</p>
    {/if}
</div>
