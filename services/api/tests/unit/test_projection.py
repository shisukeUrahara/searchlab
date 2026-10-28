import numpy as np

from searchlab.domain.models import Chunk
from searchlab.viz.projection import build_graph, knn_edges, scale


def test_knn_edges_link_nearest_and_are_undirected() -> None:
    v = np.array([[1, 0], [0.99, 0.1], [0, 1], [0.1, 0.99]], dtype=float)
    edges = knn_edges(v, k=1)
    assert {(a, b) for a, b, _ in edges} == {(0, 1), (2, 3)}
    assert all(a < b for a, b, _ in edges)
    assert all(0.9 < w <= 1.0 for _, _, w in edges)


def test_knn_never_links_a_node_to_itself() -> None:
    v = np.random.default_rng(0).normal(size=(30, 8))
    assert all(a != b for a, b, _ in knn_edges(v, k=5))


def test_scale_maps_to_box() -> None:
    s = scale(np.array([[2.0, 5.0], [4.0, 9.0]]), size=100)
    assert s.min() == 0 and s.max() == 100


def test_build_graph_shape() -> None:
    chunks = [Chunk(chunk_id=f"c{i}", source_id="nasa/a" if i else "nasa/b", title="T",
                    heading=f"H{i}", text="x", url="u", page=i + 1) for i in range(2)]
    docs = [{"source_id": "nasa/a", "title": "A"}, {"source_id": "nasa/b", "title": "B"}]
    g = build_graph(chunks, np.array([[0, 0], [1, 1]]), [(0, 1, 0.9)], docs, {"k": 1})
    assert [n["doc"] for n in g["nodes"]] == [1, 0]
    assert g["edges"] == [[0, 1, 0.9]] and g["nodes"][1]["page"] == 2 and g["meta"] == {"k": 1}
